#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable, Optional
import functools
"""
0x02. Redis basic
"""
def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        
        return output
    
    return wrapper

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

def replay(method: Callable):
    """
    Display the history of calls of a particular function.
    """
    cache = method.__self__
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)

    call_count = len(inputs)
    print(f"{method.__qualname__} was called {call_count} times:")
    
    for input_data, output_data in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_data.decode('utf-8')}) -> {output_data.decode('utf-8')}")

class Cache:
    def __init__(self):
        """
        Initializes a new Cache instance by establishing a 
        connection to the Redis server.
        Clears the current Redis database to start with a clean slate.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
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
