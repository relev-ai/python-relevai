"""
RelevAI - Python tools for using RelevAI services

Module: relevai/serializer/lz4.py
Part of: relevai

Description:
    This file contains code for the Serializer class using LZ4 with JobLib to 
    serialize objects into bytes.
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

import asyncio
import base64
import io

from typing import Any
from relevai.serializer.base import BaseSerializer


class LZ4Serializer(BaseSerializer):
    """
    Serializer using joblib with LZ4 compression.

    Suitable for binary and complex Python objects.
    """
    def __init__(self, level=1):
        """
        Args:
            level (int): Compression level for LZ4 (higher = more compression).
        """
        self._level = level

    @property
    def level(self):
        """Returns the configured compression level."""
        return self._level

    async def dump(self, value: Any) -> bytes:
        def serialize():
            with io.BytesIO() as buffer:
                joblib.dump(value, buffer, compress=("lz4", self._level))
                result = buffer.getvalue()
            return result
        result = await asyncio.to_thread(serialize)
        return result

    async def load(self, serial: bytes) -> Any:
        def deserialize():
            with io.BytesIO(serial) as buffer:
                result = joblib.load(buffer)
            return result
        result = await asyncio.to_thread(deserialize)
        return result
