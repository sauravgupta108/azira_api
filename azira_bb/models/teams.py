from django.db import models

from .utils import TimeStamp
from .projects import Projects
from .sprints import Sprints
from .users import Users


class Teams(models.Model, TimeStamp):
    name = models.CharField(max_length=80)
    members = models.ManyToManyField(Users)
    lead = models.ForeignKey(Users, on_delete=models.CASCADE)
    manager = models.ForeignKey(Users, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprints, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.sprint.name}, {self.project.name})"
