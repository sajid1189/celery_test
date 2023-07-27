import time
from celery import shared_task


@shared_task()
def heavy_task():
    print("heavy loading....")
    time.sleep(3)
    print("heavy loading done...")