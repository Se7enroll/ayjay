import requests
from diskcache import Cache


def _persist_to_file(file_name="apicache.dat"):
    def decorator(original_func):
        try:
            cache = Cache(file_name)
        except (IOError, ValueError):
            cache = {}

        def cached_func(*args, **kwargs):
            key = original_func.__name__ + str(args) + str(kwargs)
            if key not in cache:
                cache[key] = original_func(*args, **kwargs)
            return cache[key]

        return cached_func

    return decorator


def get(endpoint: str, params: dict):
    try:
        r = requests.get(endpoint, params)
        if r.reason is not requests.Response.ok:
            raise Exception("Endpoint %s dit not respond ok", endpoint)
        if r.json():
            return r.json()
    except Exception as e:
        raise Exception("Error getting %s", endpoint, e)


@_persist_to_file
def get_cached(endpoint: str, params: dict):
    return get(endpoint, params)
