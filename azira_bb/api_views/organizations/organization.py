from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from azira_bb.api_views import PermissionHandler
from azira_bb import models as az_model

from azira_bb import api_serializers as serialize
from azira_bb.utils import etc_helper as helper
from azira_bb.utils import loggers as logs


class Organization(ModelViewSet):
    serializer_class = serialize.SerializeOrganization
    queryset = az_model.Organization.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        if self.queryset.count() == 0:
            return Response({"msg": "No records found"}, status=status.HTTP_204_NO_CONTENT)

        try:
            logs.organization_logger().info(f"{helper.get_user_info(request)} Organization's List")

            return Response(serialize.SerializeOrganization(self.queryset, many=True).data,
                            status=status.HTTP_200_OK)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        self.queryset = self.queryset.filter(*args, **kwargs)

        if self.queryset.count() != 1:
            return Response({"msg": "Invalid Organization ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            logs.organization_logger().info(f"{helper.get_user_info(request)} | Organization {self.queryset[0].id}| "
                                            f"{self.queryset[0].name}")

            return Response(serialize.SerializeOrganization(self.queryset[0]).data,
                            status=status.HTTP_200_OK)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        validity = self._validate_organization_data(request)

        if validity != "OK":
            return validity

        new_org = az_model.Organization.objects.create(name=request.data["org_name"])

        helper.log_activity(request, f"New organization ({new_org.name}) added")

        try:
            logs.organization_logger().info(f"{helper.get_user_info(request)} | Organization {new_org.id}| "
                                            f"{new_org.name} | created")

            return Response(serialize.SerializeOrganization(new_org).data,
                            status=status.HTTP_201_CREATED)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        validity = self._validate_organization_data(request)

        if validity != "OK":
            return validity

        self.queryset = self.queryset.filter(*args, **kwargs)

        if self.queryset.count != 1:
            return Response({"msg": "Invalid Organization ID"}, status=status.HTTP_400_BAD_REQUEST)

        org_to_update = self.queryset[0]
        old_name = org_to_update.name
        org_to_update.name = request.data["org_name"]
        org_to_update.save()

        try:
            helper.log_activity(request, f"Organization name changed from {old_name} to {org_to_update.name}")
            logs.organization_logger().info(f"{helper.get_user_info(request)} | Organization {org_to_update.id}| "
                                            f"{org_to_update.name} | updated")

            return Response(serialize.SerializeOrganization(org_to_update).data,
                            status=status.HTTP_200_OK)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        self.queryset = self.queryset.filter(*args, **kwargs)

        if self.queryset.count != 1:
            return Response({"msg": "Invalid Organization ID"}, status=status.HTTP_400_BAD_REQUEST)

        org_name = self.queryset[0].name

        self.queryset[0].delete()

        helper.log_activity(request, f"Organization {org_name} deleted")

        try:
            logs.organization_logger().info(f"{helper.get_user_info(request)} | Organization "
                                            f"{org_name} | deleted")

            return Response({"msg": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def _validate_organization_data(request):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
        if "org_name" not in request.data:
            return Response({"msg": "Organization name is required"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data["org_name"].strip() == "":
            return Response({"msg": "Organization name can not be blank"}, status=status.HTTP_400_BAD_REQUEST)
        return "OK"
