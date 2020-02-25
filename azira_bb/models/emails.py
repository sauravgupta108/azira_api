from django.db import models

from .utils import TimeStamp
from .users import Users


class Emails(models.Model, TimeStamp):
    to = models.ManyToManyField(Users)
    subject = models.CharField(max_length=128)
    body = models.TextField()

    def __str__(self):
        return f"Email: {self.id}"

    class META:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
