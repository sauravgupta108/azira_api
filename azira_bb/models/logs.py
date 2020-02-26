from django.db import models

from .utils import TimeStamp
from azira_bb import models as az_models


class ProjectLog(models.Model, TimeStamp):
    project = models.ForeignKey(az_models.Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(az_models.AzUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project} ({self.created_by.user.get_full_name()}"


class SprintLog(models.Model, TimeStamp):
    sprint = models.ForeignKey(az_models.Sprint, on_delete=models.CASCADE)
    created_by = models.ForeignKey(az_models.AzUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sprint} ({self.created_by.user.get_full_name()}"


class IssueLog(models.Model, TimeStamp):
    issue = models.ForeignKey(az_models.Issue, on_delete=models.CASCADE)
    created_by = models.ForeignKey(az_models.AzUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.issue} ({self.created_by.user.get_full_name()}"


class ActivityLog(models.Model, TimeStamp):
    activity = models.CharField(max_length=100)
    activist = models.ForeignKey(az_models.AzUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"
