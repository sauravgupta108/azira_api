from django.db import models

from .utils import TimeStamp
from .issues import Issue
from .users import AzUser


class Comment(models.Model, TimeStamp):
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    by = models.ForeignKey(AzUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.by.user.get_short_name()} on {self.issue.id}"

    class META:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
