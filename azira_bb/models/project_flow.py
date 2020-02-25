from django.db import models

from .utils import TimeStamp
from .projects import Project
from .sprints import Sprint


class SprintFlow(models.Model, TimeStamp):
    name = models.CharField(max_length=50)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    options = models.TextField()

    class META:
        unique_together = (("sprint", "project"),)

        verbose_name = 'SprintFlow'
        verbose_name_plural = 'SprintFlows'
