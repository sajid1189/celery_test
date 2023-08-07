import time

import redis
from celery import shared_task
from celery.utils.log import get_task_logger
from contextlib import contextmanager

from django.core.cache import cache
from hashlib import md5

logger = get_task_logger(__name__)
LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes


@contextmanager
def locker(lock_id):
    timeout_at = time.monotonic() + LOCK_EXPIRE
    status = cache.add(lock_id, 1, LOCK_EXPIRE)
    if status:
        logger.info(f"acquired lock at {time.asctime()} for {lock_id}")

    try:

        yield status
    finally:
        print("I am being called")
        if time.monotonic() < timeout_at and status:
            cache.delete(lock_id)


@shared_task()
def heavy_task(title="unique_title"):
    with locker(lock_id=title) as acquired:
        if acquired:
            logger.info(f"lock acquired at {time.asctime()}")
            time.sleep(4)
            from demo.models import Invoice
            Invoice.objects.create(title=title)
            print("heavy loading done...")
            return time.asctime()
        else:
            logger.info(
                'Invoice %s is already being created by another worker', title)


@shared_task()
def another_task():
    time.sleep(4)

    logger.info(".................................g")
