from django.db import models

from .utils import TimeStamp
from azira_bb.utils import options


class Projects(models.Model, TimeStamp):
    name = models.CharField(max_length=50)
    status = models.SmallIntegerField(choices=options.PROJECT_STATUSES, default=options.PROJECT_STATUS_INITIATED)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"