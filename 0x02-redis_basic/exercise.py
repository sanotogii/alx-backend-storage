#!/usr/bin/env python3
import redis
import uuid
from typing import Union
"""
0x02. Redis basic
"""

class Cache:
    def __init__(self):
        """
        Initializes a new Cache instance by establishing a 
        connection to the Redis server.
        Clears the current Redis database to start with a clean slate.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in the Redis cache.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
