from django.db import models

from .utils import TimeStamp
from .users import AzUser


class Notification(models.Model, TimeStamp):
    to = models.ManyToManyField(AzUser)
    content = models.CharField(max_length=500)

    def __str__(self):
        return f"Notification: {self.id}"

    class META:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
