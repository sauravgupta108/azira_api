from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.contrib.auth.models import User

from azira_bb import models as az_models
from azira_bb import api_serializers as serialize
from azira_bb.api_views import PermissionHandler
from azira_bb.utils import etc_helper as helper


class Users(ModelViewSet):
    queryset = az_models.AzUser.objects.all()
    serializer_class = serialize.SerializeAzUser()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        if self.queryset.count() == 0:
            return Response({"msg": "No records found"}, status=status.HTTP_204_NO_CONTENT)

        return Response(serialize.SerializeAzUser(self.queryset, many=True),
                        status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        self.queryset = self.queryset.filter(*args, **kwargs)

        if self.queryset.count() != 1:
            return Response({"msg": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serialize.SerializeAzUser(self.queryset[0]), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request_validity = self._validate_user_request(request)

        if request_validity != "OK":
            return request_validity

        try:
            org = az_models.Organization.objects.get(id=int(request.data["org_id"]))
        except (ValueError, az_models.Organization.DoesNotExist,
                az_models.Organization.MultipleObjectsReturned):
            return Response({"msg": "Invalid Organization ID "}, status=status.HTTP_200_OK)

        try:
            designation = az_models.Designation.objects.get(id=int(request.data["designation_id"]))
        except (ValueError, az_models.Designation.DoesNotExist,
                az_models.Designation.MultipleObjectsReturned):
            return Response({"msg": "Invalid Designation ID "}, status=status.HTTP_200_OK)

        try:
            with transaction.atomic():
                new_az_user = self._create_new_user(request)

                new_az_user.organization = org
                new_az_user.designation = designation
                new_az_user.save()

                new_az_user = self._set_optional_details(request, new_az_user)
                new_az_user.save()

                return Response(serialize.SerializeAzUser(new_az_user), status=status.HTTP_201_CREATED)

        except Exception as error:
            return Response({"msg": f"Internal Error {str(error)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        request_validity = self._validate_user_request(request)

        if request_validity != "OK":
            return request_validity

        # TODO: Pending....!!!

    def update(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        return Response({"msg": "Not Implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def _validate_user_request(request):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        if "first_name" not in request.data:
            return Response({"msg": "First Name is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data["first_name"].strip() == "":
                return Response({"msg": "First Name can not be blank"}, status=status.HTTP_400_BAD_REQUEST)

        if "last_name" not in request.data:
            return Response({"msg": "Last Name is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data["last_name"].strip() == "":
                return Response({"msg": "Last Name can not be blank"}, status=status.HTTP_400_BAD_REQUEST)

        if "title" not in request.data:
            return Response({"msg": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data["title"].strip() == "":
                return Response({"msg": "Title can not be blank"}, status=status.HTTP_400_BAD_REQUEST)

        if "email" not in request.data:
            return Response({"msg": "Email address is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not helper.is_valid_email_address(request.data["email"].strip()):
                return Response({"msg": "Invalid Email address"}, status=status.HTTP_400_BAD_REQUEST)

        if "org_id" not in request.data:
            return Response({"msg": "Organization ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if "designation_id" not in request.data:
            return Response({"msg": "Designation ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        return "OK"

    @staticmethod
    def _create_new_user(request):
        new_user = User()
        new_user.first_name = request.data["first_name"]
        new_user.last_name = request.data["last_name"]
        new_user.email = request.data["email"]
        new_user.username = request.data["email"]
        new_user.save()

        new_az_user = az_models.AzUser()
        new_az_user.user = new_user
        new_az_user.title = request.data["title"]

        return new_az_user

    @staticmethod
    def _set_optional_details(request, user):
        if "hobbies" in request.data and request.data["hobbies"].strip() != "":
            user.hobbies = request.data["hobbies"]

        if "city" in request.data and request.data["city"].strip() != "":
            user.city = request.data["city"]
        return user
