from rest_framework.serializers import ModelSerializer

from azira_bb import models as az_models


class SerializeOrganizationMicro(ModelSerializer):
    class Meta:
        model = az_models.Organization
        fields = ["name"]


class SerializeOrganization(ModelSerializer):
    class Meta:
        model = az_models.Organization
        fields = ["id", "name"]
