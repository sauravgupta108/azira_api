from rest_framework import serializers

from azira_bb import models as az_model


class SerializeProjectConcise(serializers.ModelSerializer):
    class Meta:
        model = az_model.Project
        fields = ["id", "name", "start_date", "end_date"]

