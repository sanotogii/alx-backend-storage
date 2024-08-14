#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable, Optional
import functools
"""
0x02. Redis basic
"""

def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    
    return wrapper

class Cache:
    def __init__(self):
        """
        Initializes a new Cache instance by establishing a 
        connection to the Redis server.
        Clears the current Redis database to start with a clean slate.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in the Redis cache.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis; apply fn if provided
        """
        data = self._redis.get(key)
        return fn(data) if data and fn else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve and decode data as a UTF-8 string
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve and convert data to an integer
        """
        return self.get(key, fn=int)
