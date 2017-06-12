from flask import request


def make_cache_key():
    """So we can cache responses for query string GET requests.

    """

    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return path + args
