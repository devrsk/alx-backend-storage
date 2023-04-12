import redis
import requests

r = redis.Redis()
CACHE_EXPIRATION_TIME = 10

def get_page(url: str) -> str:
    # Check if the page is already cached
    cached_value = r.get(f"cached:{url}")
    if cached_value is not None:
        # Increment the access count and return the cached value
        r.incr(f"count:{url}")
        return cached_value.decode()

    # If the page is not cached, fetch it and cache it
    resp = requests.get(url)
    r.set(f"cached:{url}", resp.content)
    r.expire(f"cached:{url}", CACHE_EXPIRATION_TIME)
    r.set(f"count:{url}", 1)
    return resp.text

if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
