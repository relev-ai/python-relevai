"""
RelevAI - Python tools for using RelevAI services

Module: relevai/key/service.py
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


class ServiceKey(BaseKey):
    """
    RelevAI service key that authenticates using the client credentials flow.

    This is typically used for backend services and automated systems.
    """
    def __init__(self, client_id: str, client_secret: str, auth_url: str, **kwargs):
        """
        Initializes a new ServiceKey for backend authentication.

        Args:
            client_id (str): The service's client ID.
            client_secret (str): The client secret.
            auth_url (str): URL to retrieve new access tokens.
            **kwargs: Additional arguments passed to BaseKey.
        """
        self._client_id = client_id
        self._client_secret = client_secret
        super().__init__(auth_url=auth_url, **kwargs)

    def _build_data_request(self):
        """
        Builds the payload for token retrieval using `client_credentials` grant.

        Returns:
            dict: The POST body to send to the auth server.
        """
        return {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret
        }
