#!/usr/bin/env python3
"""
create a web cach
"""
import redis
import requests
from functools import wraps
from typing import Callable


def cache_page(method: Callable) -> Callable:
    """
    cache_page - function to cache a given url
    Arguments:
        the given function
    Returns:
        the function passed as argument
    """
    obj = redis.Redis()

    @wraps(method)
    def wrapper(args):
        """ a wrapper function to return a page &
        increment the number of times the page has been accessed
        """
        obj.incr("count:{}" + args)
        in_cache = obj.get("cached_page" + args)
        if in_cache:
            return in_cache.decode("utf-8")
        html = method(args)
        obj.set("cached_page:" + args, html, 10)
        return html
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    get_page - function to get page & returns it
    Arguments:
        url: the given url
    Returns:
        the obtained html page
    """
    html = requests.get(url).text
    return html
