#!/usr/bin/env python3
import redis
import requests
from typing import Callable
"""
Implementing an expiring web cache and tracker
"""
r = redis.Redis()


def cache_with_expiration(timeout: int) -> Callable:
    """
    Decorator to cache the result of a function for a specified time.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(url: str) -> str:
            cached_page = r.get(f"cached:{url}")
            if cached_page:
                return cached_page.decode('utf-8')

            result = func(url)
            r.setex(f"cached:{url}", timeout, result)
            return result
        return wrapper
    return decorator


def track_access(func: Callable) -> Callable:
    """
    Decorator to track how many times a URL has been accessed.
    """
    def wrapper(url: str) -> str:
        r.incr(f"count:{url}")
        return func(url)
    return wrapper


@track_access
@cache_with_expiration(10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and caches it for 10 seconds.
    """
    response = requests.get(url)
    return response.text
