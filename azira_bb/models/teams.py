from django.db import models

from .utils import TimeStamp
from .projects import Project
from .sprints import Sprint
from .users import AzUser


class Team(models.Model, TimeStamp):
    name = models.CharField(max_length=80)
    members = models.ManyToManyField(AzUser, related_name="team_member")
    lead = models.ForeignKey(AzUser, on_delete=models.CASCADE, related_name="team_lead")
    manager = models.ForeignKey(AzUser, on_delete=models.CASCADE, related_name="project_manager")
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.sprint.name}, {self.project.name})"

    class META:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
