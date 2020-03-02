from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from azira_bb import models as az_models
from .serialize_organization import SerializeOrganizationMicro
from .serialize_designation import SerializeDesignationMicro


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class UserSerializerMicro(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class SerializeLoggedInUser(ModelSerializer):
    user = UserSerializer()
    designation = SerializeDesignationMicro()
    organization = SerializeOrganizationMicro()

    class Meta:
        model = az_models.AzUser
        fields = ["id", "user", "title", "designation", "organization"]


class SerializeAzUser(ModelSerializer):
    user = UserSerializer()
    designation = SerializeDesignationMicro()
    organization = SerializeOrganizationMicro()

    class Meta:
        model = az_models.AzUser
        fields = ["id", "user", "title", "designation", "organization"]


class SerializeUserProjectAccess(ModelSerializer):
    user = UserSerializerMicro()

    class Meta:
        model = az_models.AzUser
        fields = ["id", "user"]
