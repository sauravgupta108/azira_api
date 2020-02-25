from django.db import models

from .utils import TimeStamp
from azira_bb.utils import options


class Organizations(models.Model, TimeStamp):
    name = models.CharField(max_length=50)
    status = models.SmallIntegerField(choices=options.ORGANIZATION_STATUSES, default=options.ORGANIZATION_STATUS_ACTIVE)

    def __str__(self):
        return f"{self.name}"

