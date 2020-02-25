from django.db import models

from .utils import TimeStamp
from .projects import Project
from .users import AzUser


class ProjectAccess(models.Model, TimeStamp):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(AzUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.name}: {self.owner.user.get_full_name()}"

    class META:
        verbose_name = 'ProjectAccess'
        verbose_name_plural = 'ProjectAccess'
