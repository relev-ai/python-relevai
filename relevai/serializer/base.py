"""
RelevAI - Python tools for using RelevAI services

Module: relevai/serializer/base.py
Part of: relevai

Description:
    This file contains code for the Serializer abstract base class
    intended for serializing objects into bytes / strings.
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
import base64
import asyncio

from abc import ABC, abstractmethod
from typing import Any


class BaseSerializer(ABC):
    """
    Abstract base class for data serializers.

    Defines a common interface for serialization and deserialization,
    including support for base64-encoded strings (dumps/loads).
    """

    @abstractmethod
    async def dump(self, value: Any) -> bytes:
        """
        Serializes a Python object into bytes.

        Args:
            value (Any): The Python object to serialize.

        Returns:
            bytes: The serialized representation.
        """
        ...

    async def dumps(self, value: Any) -> str:
        """
        Serializes a Python object into a base64-encoded string.

        Args:
            value (Any): The object to serialize.

        Returns:
            str: Base64-encoded serialized data.
        """
        serial = await self.dump(value)

        def _dumps():
            serial_encoded = base64.b64encode(serial)
            return serial_encoded.decode("UTF-8")
        
        return await asyncio.to_thread(_dumps)

    @abstractmethod
    async def load(self, serial: bytes) -> Any:
        """
        Deserializes an object from raw bytes.

        Args:
            serial (bytes): Serialized byte data.

        Returns:
            Any: The reconstructed Python object.
        """
        ...

    async def loads(self, serial: str) -> Any:
        """
        Deserializes an object from a base64-encoded string.

        Args:
            serial (str): Base64-encoded serialized data.

        Returns:
            Any: The reconstructed object.
        """
        def _decode():
            return base64.b64decode(serial)

        serial_decoded = await asyncio.to_thread(_decode)
        return await self.load(serial_decoded)            
        

