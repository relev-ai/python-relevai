"""
RelevAI - Python tools for using RelevAI services

Module: relevai/utils.py
Part of: relevai

Description:
    This file contains code for small self-contained auxiliary functions.
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

import time
import asyncio
from functools import wraps
from inspect import iscoroutinefunction, isfunction


def chunkize(l, size):
    for i in range(0, len(l), size):
        yield l[i:i+size]

def elapsed(timestamp):
    return time.time() - timestamp

def ttl_cached(ttl_seconds: int):
    """
    Decorator for properties.
    Caches a property for the specified TTL time in seconds.

    For example:

    class Foo:
        @property
        @ttl_cached(ttl_seconds=2)
        def bar(self):
            return "foobar"
        
    """
    def decorator(func):
        attr_value = f"_ttlcache_value_{func.__name__}"
        attr_time = f"_ttlcache_time_{func.__name__}"

        is_async = iscoroutinefunction(func)

        async def async_wrapper(self, *args, **kwargs):
            now = time.time()
            last_time = getattr(self, attr_time, 0)
            expired = (now - last_time) > ttl_seconds

            if not hasattr(self, attr_value) or expired:
                result = await func(self, *args, **kwargs)
                setattr(self, attr_value, result)
                setattr(self, attr_time, now)

            return getattr(self, attr_value)

        def sync_wrapper(self, *args, **kwargs):
            now = time.time()
            last_time = getattr(self, attr_time, 0)
            expired = (now - last_time) > ttl_seconds

            if not hasattr(self, attr_value) or expired:
                result = func(self, *args, **kwargs)
                setattr(self, attr_value, result)
                setattr(self, attr_time, now)

            return getattr(self, attr_value)

        if isinstance(func, property):
            inner_func = func.fget
            if iscoroutinefunction(inner_func):
                @property
                @wraps(inner_func)
                def prop(self):
                    return async_wrapper(self)
                return prop
            else:
                @property
                @wraps(inner_func)
                def prop(self):
                    return sync_wrapper(self)
                return prop

        return async_wrapper if is_async else sync_wrapper

    return decorator
