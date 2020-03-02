from rest_framework.serializers import ModelSerializer

from azira_bb import models


class SerializeTeamMicro(ModelSerializer):
    class Meta:
        model = models.Team
        fields = ["id", "name"]
