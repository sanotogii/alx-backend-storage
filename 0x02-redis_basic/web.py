#!/usr/bin/env python3
import requests
import time
from functools import wraps



basic_cache = {}
basic_url_counts = {}

def get_page_basic(url: str) -> str:
    current_time = time.time()
    
    if url in basic_cache and current_time - basic_cache[url]['timestamp'] < 10:
        content = basic_cache[url]['content']
    else:
        response = requests.get(url)
        content = response.text
        basic_cache[url] = {
            'content': content,
            'timestamp': current_time
        }
    
    basic_url_counts[f"count:{url}"] = basic_url_counts.get(f"count:{url}", 0) + 1
    
    return content


def cache_and_track(expiration_time=10):
    cache = {}
    url_counts = {}

    def decorator(func):
        @wraps(func)
        def wrapper(url: str) -> str:
            current_time = time.time()

            if url in cache and current_time - cache[url]['timestamp'] < expiration_time:
                content = cache[url]['content']
            else:
                content = func(url)
                cache[url] = {
                    'content': content,
                    'timestamp': current_time
                }

            url_counts[f"count:{url}"] = url_counts.get(f"count:{url}", 0) + 1
            return content

        def get_count(url: str) -> int:
            return url_counts.get(f"count:{url}", 0)

        wrapper.get_count = get_count
        return wrapper

    return decorator

@cache_and_track(expiration_time=10)
def get_page_decorator(url: str) -> str:
    response = requests.get(url)
    return response.text
