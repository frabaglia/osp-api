"""Default configuration for application; should be overridden
with Docker Secrets/envvars...

"""

DEBUG = True
RATELIMIT_DEFAULT = "5 per second"

FLASK_CACHE = dict(  # TODO: redis! but on a different host? or same db?... cuz celery uses..
    CACHE_TYPE = 'redis',
    CACHE_DEFAULT_TIMEOUT = 3600,
    CACHE_REDIS_URL = 'redis://redis:6379/1'
)
