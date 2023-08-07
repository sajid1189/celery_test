import redis
from django.http import HttpResponse
from django.shortcuts import render

from demo.tasks import heavy_task, another_task


# Create your views here.
def hello(request, *args, **kwargs):
    import json
    another_task.delay()
    import json
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    tasks = r.lrange("celery", 0, -1)
    for task in tasks:

        if json.loads(task)["headers"]["task"] == 'demo.tasks.another_task':
            return HttpResponse("Another task running")

    return HttpResponse("Success")