from django.db import models

from .utils import TimeStamp
from .projects import Projects
from .sprints import Sprints
from .users import Users


class Teams(models.Model, TimeStamp):
    name = models.CharField(max_length=80)
    members = models.ManyToManyField(Users, related_name="team_member")
    lead = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="team_lead")
    manager = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="project_manager")
    sprint = models.ForeignKey(Sprints, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.sprint.name}, {self.project.name})"
