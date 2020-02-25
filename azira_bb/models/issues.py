from django.db import models

from .utils import TimeStamp
from .projects import Project
from .sprints import Sprint
from .users import AzUser
from .project_flow import SprintFlow


class Issue(models.Model, TimeStamp):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    flow = models.ForeignKey(SprintFlow, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(AzUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.title} ({self.sprint.name}-{self.project.name})"

    class META:
        verbose_name = "Issue"
        verbose_name_plural = "Issues"
