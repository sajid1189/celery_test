from django.db import models


# Create your models here.
class Invoice(models.Model):
    title = models.CharField(max_length=100)
