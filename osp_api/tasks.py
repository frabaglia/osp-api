"""Celery tasks; things that take a long time and things
which should be done simultaneously!

"""

from . import config

from celery import Celery


# TODO: can use config for these settings...
celery = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
)


@celery.task
def query_titles(query_string_args):
    """Query elasticsearch."""
    import time
    time.sleep(30)
    return query_string_args
