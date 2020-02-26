from django.contrib import admin

from azira_bb import models as az

# Register your models here.
admin.site.register(az.Comment)
admin.site.register(az.Designation)
admin.site.register(az.Email)
admin.site.register(az.Issue)
admin.site.register(az.Notification)
admin.site.register(az.Organization)
admin.site.register(az.Project)
admin.site.register(az.SprintFlow)
admin.site.register(az.Sprint)
admin.site.register(az.Team)
admin.site.register(az.AzUser)
admin.site.register(az.ProjectAccess)
admin.site.register(az.ActivityLog)
admin.site.register(az.ProjectLog)
admin.site.register(az.IssueLog)
admin.site.register(az.SprintLog)
