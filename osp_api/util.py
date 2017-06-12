from flask import request


def make_cache_key():
    """flask-cache: Create consistent keys for query string arguments.

    Produces the same cache key regardless of argument order, e.g.,
    both `?limit=10&offset=20` and `?offset=20&limit=10` will always
    produce the same exact cache key.

    """

    # Create a tuple of (key, value) pairs, where the key is the
    # argument name and the value is its respective value. Order this
    # tuple by key. Doing this ensures the cache key created is always
    # the same for query string args whose keys/values are the same,
    # regardless of the order in which they are provided.
    args_as_sorted_tuple = tuple(
        sorted(
            (pair for pair in request.args.items()),
            key=lambda pair: pair[0],
        )
    )
    # ... now hash the sorted (key, value) tuple so it can be
    # used as a key for cache.
    hashed_args = str(hash(args_as_sorted_tuple))
    cache_key = request.path + hashed_args
    return cache_key
