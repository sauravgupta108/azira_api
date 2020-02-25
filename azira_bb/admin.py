from django.contrib import admin

from azira_bb import models

# Register your models here.
admin.site.register(models.Comments)
admin.site.register(models.Designations)
admin.site.register(models.Emails)
admin.site.register(models.Issues)
admin.site.register(models.Notifications)
admin.site.register(models.Organizations)
admin.site.register(models.Projects)
admin.site.register(models.SprintFlow)
admin.site.register(models.Sprints)
admin.site.register(models.Teams)
admin.site.register(models.Users)
admin.site.register(models.ProjectAccess)
