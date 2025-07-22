"""
RelevAI - Python tools for using RelevAI services

Module: relevai/serializer/msgpack.py
Part of: relevai

Description:
    This file contains code for the Serializer class using MSGPack to 
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
import msgpack

from typing import Any
from relevai.serializer.base import BaseSerializer


class MsgPackSerializer(BaseSerializer):
    """
    Serializer using MessagePack (msgpack).

    Efficient for structured and numeric data, faster and smaller than JSON.
    """

    async def dump(self, value: Any) -> bytes:
        def _dump():
            return msgpack.packb(value)
        
        return await asyncio.to_thread(_dump)

    async def load(self, serial: bytes) -> Any:
        def _load():
            return msgpack.unpackb(serial)

        return await asyncio.to_thread(_load)
