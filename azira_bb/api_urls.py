from django.urls import path, include
from azira_bb import api_views
from rest_framework.routers import SimpleRouter


routers = SimpleRouter()
routers.register("designation", api_views.Designation)
routers.register("organization", api_views.Organization)
routers.register("user", api_views.Users)
routers.register("project", api_views.Project)

urlpatterns = [
    path("get_token/", api_views.AziraLogin.as_view(), name="get_token"),
    path("", include(routers.urls)),
    path("project_access/", api_views.ProjectAccess.as_view(), name="project_access")
]
