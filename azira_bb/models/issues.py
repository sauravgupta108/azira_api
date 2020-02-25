from django.db import models

from .utils import TimeStamp
from .projects import Projects
from .sprints import Sprints
from .users import Users
from .project_flow import SprintFlow


class Issues(models.Model, TimeStamp):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    sprint = models.ForeignKey(Sprints, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    flow = models.ForeignKey(SprintFlow, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.title} ({self.sprint.name}-{self.project.name})"
