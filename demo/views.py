import redis
from django.http import HttpResponse
from django.shortcuts import render

from demo.models import Invoice
from demo.tasks import singleton_task, another_task


# Create your views here.
def hello(request, *args, **kwargs):
    current_count = Invoice.objects.count()
    for i in range(10):
        singleton_task.delay(title=f"invoice {current_count + i}")
    return HttpResponse("Added 10 tasks")