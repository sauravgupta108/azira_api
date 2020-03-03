from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from azira_bb import models
from .serialize_project import SerializeProjectMicro
from .serialize_sprint import SerializeSprintMini
from .serialize_users import SerializeUserProjectAccess


class SerializeTeamMicro(ModelSerializer):
    class Meta:
        model = models.Team
        fields = ["id", "name"]


class SerializeTeamDetailed(ModelSerializer):
    project = SerializeProjectMicro()
    sprint = SerializeSprintMini()
    manager = SerializeUserProjectAccess()
    lead = SerializeUserProjectAccess()
    members = SerializeUserProjectAccess(many=True)

    class Meta:
        model = models.Team
        fields = ["id", "name", "project", "sprint", "manager", "lead", "members"]
