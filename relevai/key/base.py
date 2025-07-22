"""
RelevAI - Python tools for using RelevAI services

Module: relevai/key/base.py
Part of: relevai

Description:
    This file contains base code for RelevAI Keys.
"""

# Copyright 2025 RelevAI S.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import time
import threading
import json
import base64
import requests
import weakref
import asyncio

from loguru import logger
from abc import ABC, abstractmethod

from relevai.exceptions import RelevAITokenError


class BaseKey(ABC):
    """
    Base class for managing authentication tokens used with RelevAI services.

    Automatically handles token renewal, expiration checks, and supports
    background refreshing using a dedicated thread.

    Subclasses must implement the `_build_data_request` method to define how
    the token request payload is constructed.
    """
    def __init__(self, 
                 auth_url: str, 
                 safety_margin: int = 30, 
                 max_attempts:int = 5, 
                 alive:bool=True, 
                 access_token:str=None):
        """
        Initializes a new instance of the BaseKey class.

        Args:
            auth_url (str): URL endpoint to request new tokens.
            safety_margin (int): Time in seconds before expiration to trigger a renewal.
            max_attempts (int): Maximum number of renewal attempts before stopping.
            alive (bool): Whether to keep a background thread alive for auto-renewal.
            access_token (str, optional): Pre-existing token to use initially.
        """                 
        self._expires_at = 0
        self._lock = threading.Lock()
        self._access_token = access_token
        self._auth_url = auth_url
        self._safety_margin = safety_margin
        self._max_attempts = max_attempts
        self._thread = None
        self._header, self._claims = self._decode() if access_token else ({}, {})
        self._alive = alive
        self._renewal_hooks = weakref.WeakSet()
        self._kill_event = threading.Event()

        if alive:
            self.renew_token()
            self.restart()

    def add_hook(self, hook:callable):
        """
        Registers a callable to be executed after each successful token renewal.

        Args:
            hook (callable): A function that accepts one argument (self).
        """
        self._renewal_hooks.add(hook)
        logger.debug(f"Registered hook ({len(self._renewal_hooks)} hooks)")
        
    def is_alive(self):
        """
        Indicates whether this key is configured to auto-renew in background.

        Returns:
            bool: True if background refresh is enabled.
        """
        return self._alive

    @property
    def token(self):
        """
        Returns a valid access token, renewing it if needed.

        Returns:
            str: A valid (possibly refreshed) access token.
        """
        if self._access_token is None or self.expires_in <= self._safety_margin:
            self.renew_token()

        if not self.is_running and self.is_alive():
            logger.warning("Token refresher thread was not running. Restarting.")
            self.restart()

        return self._access_token

    async def async_get_token(self):
        """
        Asynchronously retrieves a valid access token.

        Returns:
            str: The access token.
        """
        return await asyncio.to_thread(lambda: self.token)

    @property
    def expires_in(self):
        """
        Time in seconds until the current token expires.

        Returns:
            float: Seconds remaining before expiration.
        """
        with self._lock:
            time_remaining = self._expires_at - time.time()
        return time_remaining

    @property
    def is_running(self):
        """
        Checks if the background refresher thread is currently active.

        Returns:
            bool: True if refresher thread is running.
        """
        return self._thread is not None and self._thread.is_alive()

    def restart(self):
        """
        Starts or restarts the background token refresher thread.
        """
        if self.is_running or not self.is_alive():
            return None

        self._kill_event.clear()
        self._thread = threading.Thread(target=self._token_refresher_loop, daemon=True)
        self._thread.start()

    def kill(self):
        """
        Stops the background refresher thread.

        Returns:
            bool: True if the thread was successfully stopped.
        """
        if not self.is_alive:
            return True

        self._kill_event.set()
        self._thread.join()

        return True

    async def async_kill(self):
        """
        Asynchronously stops the background refresher thread.

        Returns:
            bool: True if the thread was successfully stopped.
        """
        return await asyncio.to_thread(self.kill)

    def _token_refresher_loop(self):
        """
        Internal method: loop that keeps the token refreshed in background.
        Stops after `max_attempts` consecutive failures or on kill signal.
        """
        attempts = 0

        while attempts < self._max_attempts and not self._kill_event.is_set():
            time.sleep(5)

            if self.expires_in > self._safety_margin:
                continue
        
            try:
                self.renew_token()
                attempts = 0

            except Exception as e:
                logger.error(f"Error refreshing token: {e}")
                time.sleep(10)
                attempts += 1

        
        if attempts >= self._max_attempts:
            logger.critical(f"Token refresher thread stopped after {attempts} failed attempts.")
        else:
            logger.info(f"Token refresher thread killed")

    @abstractmethod
    def _build_data_request(self):
        """
        Constructs the data payload for the token request.

        This method must be implemented by subclasses.

        Returns:
            dict or str: Data to send in the POST request body.
        """
        ...

    def renew_token(self):
        """
        Manually renews the access token and triggers registered hooks.

        Raises:
            RelevAITokenError: If token retrieval fails.
        """
        try:
            data = self._build_data_request()

            response = requests.post(self._auth_url, data=data)
            response.raise_for_status()
            token_data = response.json()

            with self._lock:
                self._access_token = token_data["access_token"]
                self._expires_at = time.time() + token_data["expires_in"]
                self._header, self._claims = self._decode()
                logger.debug(f"Access token retrieved. Expires in {token_data['expires_in']}s")

            logger.debug(f"Calling ({len(self._renewal_hooks)} hooks)")

            for hook in self._renewal_hooks:
                hook(self)

        except Exception as e:
            logger.error(f"Token retrieval failed: {e}")
            raise RelevAITokenError("Failed to retrieve the token.") from e

    def _decode(self):
        """
        Decodes the current JWT token into header and claims.

        Returns:
            tuple[dict, dict]: Decoded JWT header and payload.

        Raises:
            RelevAITokenError: If the token is malformed or invalid.
        """
        try:
            parts = self._access_token.split(".")
            if len(parts) != 3:
                raise RelevAITokenError("Malformed JWT")

            header_b64, payload_b64, _ = parts

            padded_header = header_b64 + '=' * (-len(header_b64) % 4)
            padded_payload = payload_b64 + '=' * (-len(payload_b64) % 4)

            header = json.loads(base64.urlsafe_b64decode(padded_header))
            payload = json.loads(base64.urlsafe_b64decode(padded_payload))

            return header, payload

        except Exception as e:
            logger.error(f"Token invalid: {e}")
            raise RelevAITokenError("Token invalid.") from e

    def __repr__(self):
        return f"<{self.__class__.__name__} expires_in={self.expires_in:.0f}s alive={self.is_alive()}>"

    def __str__(self):
        return repr(self)