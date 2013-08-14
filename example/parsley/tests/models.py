#Django requires every app to have models.
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
