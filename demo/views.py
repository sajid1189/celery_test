from django.http import HttpResponse
from django.shortcuts import render

from demo.tasks import heavy_task


# Create your views here.
def hello(request, *args, **kwargs):
    heavy_task.delay()
    return HttpResponse("Success")