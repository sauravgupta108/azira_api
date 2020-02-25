from django.contrib import admin

from azira_bb import models

# Register your models here.
admin.site.register(models.Comment)
admin.site.register(models.Designation)
admin.site.register(models.Email)
admin.site.register(models.Issue)
admin.site.register(models.Notification)
admin.site.register(models.Organization)
admin.site.register(models.Project)
admin.site.register(models.SprintFlow)
admin.site.register(models.Sprint)
admin.site.register(models.Team)
admin.site.register(models.AzUser)
admin.site.register(models.ProjectAccess)
