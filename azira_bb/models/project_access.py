from django.db import models

from .utils import TimeStamp
from .projects import Projects
from .users import Users


class ProjectAccess(models.Model, TimeStamp):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.name}: {self.owner.user.get_full_name()}"
