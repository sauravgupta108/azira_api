from django.db import models

from .utils import TimeStamp


class Designations(models.Model, TimeStamp):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"
