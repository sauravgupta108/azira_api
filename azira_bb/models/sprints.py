from django.db import models

from .utils import TimeStamp
from .projects import Project
from azira_bb.utils import options


class Sprint(models.Model, TimeStamp):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=options.SPRINT_STATUSES, default=options.SPRINT_STATUS_INACTIVE)
    start_date = models.DateField()
    end_date = models.DateField()

    def get_teams(self):
        from azira_bb.models import Team
        return Team.objects.filter(sprint_id=self.id)

    def __str__(self):
        return f"{self.name}-{self.project.name} : {self.start_date}-{self.end_date}"

    class META:
        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'
