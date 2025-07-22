"""
RelevAI - Python tools for using RelevAI services

Module: relevai/key/client.py
Part of: relevai

Description:
    This file contains code for a RelevAI Key access to relevai services.
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

from relevai.key.base import BaseKey


class ClientKey(BaseKey):
    """
    RelevAI client key that authenticates using a refresh token (API key).

    This key type is used by regular RelevAI users (with long-lived tokens)
    and refreshes access tokens using the `refresh_token` grant type.
    """

    def __init__(self,
                 api_key:str, 
                 auth_url: str, 
                 client_id: str, 
                 client_secret: str = None,
                 safety_margin: int = 30, 
                 max_attempts:int = 5,
                 alive:bool=True, 
                 access_token:str=None):
        """
        Initializes a new ClientKey for authenticating with RelevAI.

        Args:
            api_key (str): The refresh token (long-lived API key).
            auth_url (str): URL to retrieve new access tokens.
            client_id (str): The application's client ID.
            client_secret (str, optional): Optional client secret.
            safety_margin (int): Time in seconds before expiry to trigger renewal.
            max_attempts (int): Max number of token refresh attempts.
            alive (bool): Whether to auto-renew in background.
            access_token (str, optional): Optional pre-existing access token.
        """                 
        self._client_id = client_id
        self._api_key = api_key
        self._client_secret = client_secret

        super().__init__(auth_url=auth_url, 
                         safety_margin=safety_margin, 
                         max_attempts=max_attempts, 
                         alive=alive, 
                         access_token=access_token)
    
    def _build_data_request(self):
        """
        Builds the payload for token retrieval using `refresh_token` grant.

        Returns:
            dict: The POST body to send to the auth server.
        """        
        data = {
            "grant_type": "refresh_token",
            "client_id": self._client_id,
            "refresh_token": self._api_key
        }
        if self._client_secret:
            data['client_secret'] = self._client_secret
        
        return data

    @property
    def user_id(self):
        """
        Returns the user ID (subject) associated with this token.

        Returns:
            str: The user ID from the token claims, or "unknown".
        """        
        return self._claims.get("sub", "unknown")
