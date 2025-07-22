"""
RelevAI - Python tools for using RelevAI services

Module: relevai/ailang/client.py
Part of: relevai

Description:
    This file contains code for a client class with access to AI LLM models.
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
import ollama

from loguru import logger


class AILangClient:
    """
    Synchronous client for interacting with RelevAI's AI Lang API.

    Automatically refreshes the token when using a `BaseKey` and rebuilds the client.
    """
    def __init__(self, key:BaseKey=None, base_url:str="https://api.relev.ai/ai-lang/v1/", **kwargs):
        """
        Initializes the synchronous AI Lang client.

        Args:
            key (BaseKey, optional): RelevAI authentication key.
            base_url (str): Base URL of the AI Lang API.
            **kwargs: Additional keyword arguments passed to `ollama.Client`.
        """
        self._hook_ref = self._on_renewal
        self._key = key
        self._base_url = base_url
        self._kwargs = kwargs
        self._client = None
        self._on_renewal(key)

        if key is not None:
            key.add_hook(self._hook_ref)
        
    def _on_renewal(self, key):
        logger.debug("Renewal notified. Regenerated client.")
        
        headers = {"Authorization": f"Bearer {key.token}"} if key is not None else None

        self._client = ollama.Client(
            host=self._base_url,
            headers=headers, 
            **self._kwargs
        )

    def __getattr__(self, name):
        if self._client is None:
            raise RuntimeError("Client has not been initialized correctly.")
        return getattr(self._client, name)

    def chat(self, *args, **kwargs):
        """
        Sends a synchronous chat request to the AI Lang API.
        """
        return self._client.chat(*args, **kwargs)

    def embed(self, *args, **kwargs):
        """
        Sends a synchronous embedding request to the AI Lang API.
        """
        return self._client.embed(*args, **kwargs)


class AILangAsyncClient:
    """
    Asynchronous client for interacting with RelevAI's AI Lang API.

    Automatically refreshes the token when using a `BaseKey` and rebuilds the client.
    """
    def __init__(self, key:BaseKey=None, base_url:str="https://api.relev.ai/ai-lang/v1/", **kwargs):
        """
        Initializes the asynchronous AI Lang client.

        Args:
            key (BaseKey, optional): RelevAI authentication key.
            base_url (str): Base URL of the AI Lang API.
            **kwargs: Additional keyword arguments passed to `ollama.AsyncClient`.
        """
        self._hook_ref = self._on_renewal
        self._key = key
        self._base_url = base_url
        self._kwargs = kwargs
        self._client = None
        self._on_renewal(key)

        if key is not None:
            key.add_hook(self._hook_ref)

    def _on_renewal(self, key):
        logger.debug("Renewal notified. Regenerated client.")

        headers = {"Authorization": f"Bearer {key.token}"} if key is not None else None

        self._client = ollama.AsyncClient(
            host=self._base_url, 
            headers=headers, 
            **self._kwargs
        )

    def __getattr__(self, name):
        return getattr(self._client, name)

    async def chat(self, *args, **kwargs):
        """
        Sends an asynchronous chat request to the AI Lang API.
        """
        return await self._client.chat(*args, **kwargs)

    async def embed(self, *args, **kwargs):
        """
        Sends an asynchronous embedding request to the AI Lang API.
        """
        return await self._client.embed(*args, **kwargs)
