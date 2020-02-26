from rest_framework.serializers import ModelSerializer

from azira_bb import models as az_models


class SerializeDesignationMicro(ModelSerializer):
    class Meta:
        model = az_models.Designation
        fields = ["title"]


class SerializeDesignation(ModelSerializer):
    class Meta:
        model = az_models.Designation
        fields = ["id", "title"]
