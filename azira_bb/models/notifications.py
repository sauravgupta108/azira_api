from django.db import models

from .utils import TimeStamp
from .users import Users


class Notifications(models.Model, TimeStamp):
    to = models.ManyToManyField(Users)
    content = models.CharField(max_length=500)

    def __str__(self):
        return f"Notification: {self.id}"
