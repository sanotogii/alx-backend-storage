#!/usr/bin/env python3
"""
 Implementing an expiring web cache and tracker
"""
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()


def cache_decorator(expiration: int = 10):
    """
    Decorator factory to cache function results
    in Redis with a specified expiration time.
    """
    def decorator(func: Callable) -> Callable:
        """
        Inner decorator that wraps the
        function to add caching behavior
        """
        @wraps(func)
        def wrapper(url: str) -> str:
            """
            Wrapper function that implements the
            caching logic for web page content
            """
            redis_store.incr(f'count:{url}')
            cached_result = redis_store.get(f'result:{url}')

            if cached_result:
                return cached_result.decode('utf-8')

            result = func(url)
            redis_store.setex(f'result:{url}', expiration, result)
            return result

        return wrapper
    return decorator


@cache_decorator()
def get_page(url: str) -> str:
    """
    Fetches the content of a web page,
    with results cached by the decorator
    """
    return requests.get(url).text


def get_access_count(url: str) -> int:
    """Retrieves the number of times a URL has been accessed"""
    return int(redis_store.get(f'count:{url}') or 0)
