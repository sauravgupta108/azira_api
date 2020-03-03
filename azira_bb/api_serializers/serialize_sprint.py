from rest_framework import serializers

from azira_bb import models as az_models


class SerializeSprintMini(serializers.ModelSerializer):
    class Meta:
        model = az_models.Sprint
        fields = ["name", "status", "start_date", "end_date"]


class SerializeSprintMicro(serializers.ModelSerializer):
    class Meta:
        model = az_models.Sprint
        fields = ["id", "name"]
