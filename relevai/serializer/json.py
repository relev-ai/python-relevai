"""
RelevAI - Python tools for using RelevAI services

Module: relevai/serializer/json.py
Part of: relevai

Description:
    This file contains code for the Serializer class using JSON to 
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
import io
import json

from typing import Any
from relevai.serializer.base import BaseSerializer


class JSONSerializer(BaseSerializer):
    """
    Serializer that uses JSON for (de)serialization.

    Converts Python objects to JSON strings, then encodes to bytes.
    """

    async def dump(self, value: Any) -> bytes:
        result = await self.dumps(value)
        result = result.encode("UTF-8")
        return result

    async def load(self, serial: bytes) -> Any:
        result = await self.loads(serial.decode("UTF-8"))
        return result

    async def dumps(self, value: Any) -> str:
        def serialize():
            result = json.dumps(value)
            return result
        result = await asyncio.to_thread(serialize)
        return result

    async def loads(self, serial: str) -> Any:
        def deserialize():
            result = json.loads(serial)
            return result
        result = await asyncio.to_thread(deserialize)
        return result
