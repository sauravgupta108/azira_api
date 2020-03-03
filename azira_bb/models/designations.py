from django.db import models

from .utils import TimeStamp
from azira_bb.utils import options


class Designation(models.Model, TimeStamp):
    title = models.CharField(max_length=64)
    code = models.SmallIntegerField(choices=options.ORGANIZATION_STATUSES, default=options.TEAM_MEMBER)

    def __str__(self):
        return f"{self.title}"

    class META:
        verbose_name = "Designation"
        verbose_name_plural = "Designations"
