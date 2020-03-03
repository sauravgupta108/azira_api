from rest_framework import serializers

from azira_bb import models as az_model
from .serialize_users import SerializeUserProjectAccess
from .serialize_sprint import SerializeSprintMini


class SerializeProjectConcise(serializers.ModelSerializer):
    class Meta:
        model = az_model.Project
        fields = ["id", "name", "start_date", "end_date"]


class SerializeProjectMicro(serializers.ModelSerializer):
    class Meta:
        model = az_model.Project
        fields = ["id", "name"]


class SerializeProjectDetailed(serializers.ModelSerializer):
    from .serialize_team import SerializeTeamMicro
    owner = SerializeUserProjectAccess(source="get_project_owner")
    sprints = SerializeSprintMini(source="get_sprints", many=True)
    teams = SerializeTeamMicro(source="get_teams", many=True)

    class Meta:
        model = az_model.Project
        fields = ["id", "name", "start_date", "end_date", "owner", "sprints", "teams"]


class SerializeProjectAccess(serializers.ModelSerializer):
    project = SerializeProjectConcise()
    owner = SerializeUserProjectAccess()

    class Meta:
        model = az_model.ProjectAccess
        fields = ["id", "project", "owner"]
