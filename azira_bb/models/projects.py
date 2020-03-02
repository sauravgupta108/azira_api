from django.db import models

from .utils import TimeStamp
from azira_bb.utils import options


class Project(models.Model, TimeStamp):
    name = models.CharField(max_length=50)
    status = models.SmallIntegerField(choices=options.PROJECT_STATUSES, default=options.PROJECT_STATUS_INITIATED)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def get_project_owner(self):
        from azira_bb.models import ProjectAccess
        try:
            project_access = ProjectAccess.objects.get(project_id=self.id)
            return project_access.owner
        except (ProjectAccess.DoesNotExist, ProjectAccess.MultipleObjectsReturned):
            return None

    def get_sprints(self):
        from azira_bb.models import Sprint
        return Sprint.objects.filter(project_id=self.id)

    def get_teams(self):
        from azira_bb.models import Team
        return Team.objects.filter(project_id=self.id)

    def __str__(self):
        return f"{self.name}"

    class META:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
