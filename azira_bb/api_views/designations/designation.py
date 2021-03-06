from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from azira_bb.api_views import PermissionHandler
from azira_bb import models as az_model

from azira_bb import api_serializers as serialize
from azira_bb.utils import etc_helper as helper
from azira_bb.utils import loggers as logs


class Designation(ModelViewSet):
    serializer_class = serialize.SerializeDesignation
    queryset = az_model.Designation.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        if self.queryset.count() == 0:
            return Response({"msg": "No records found"}, status=status.HTTP_204_NO_CONTENT)
        
        try:
            logs.designation_logger().info(f"{helper.get_user_info(request)} - Designation's List")

            return Response(serialize.SerializeDesignation(self.queryset, many=True).data,
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
            return Response({"msg": "Invalid designation ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            logs.designation_logger().info(f"{helper.get_user_info(request)} - Designation {kwargs}")

            return Response(serialize.SerializeDesignation(self.queryset[0]).data,
                            status=status.HTTP_200_OK)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        validity = self._validate_designation_data(request)

        if validity != "OK":
            return validity

        new_designation = az_model.Designation.objects.create(title=request.data["designation_name"])
        helper.log_activity(request, f"New Designation ({new_designation.title}) added")

        try:
            logs.designation_logger().info(f"{helper.get_user_info(request)} - Designation | {new_designation.id}| "
                                           f"{new_designation.title}| created")
            return Response(serialize.SerializeDesignation(new_designation).data,
                            status=status.HTTP_201_CREATED)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        validity = self._validate_designation_data(request)

        if validity != "OK":
            return validity

        self.queryset = self.queryset.filter(*args, **kwargs)

        if self.queryset.count != 1:
            return Response({"msg": "Invalid designation"}, status=status.HTTP_400_BAD_REQUEST)

        designation_to_update = self.queryset[0]
        older_title = designation_to_update.title

        designation_to_update.title = request.data["designation_name"]
        designation_to_update.save()

        helper.log_activity(request, f"Designation title changed from {older_title} to {designation_to_update.title}")

        try:
            logs.designation_logger().info(f"{helper.get_user_info(request)} - Designation |{designation_to_update.id}|"
                                           f" {designation_to_update.title}| updated")
            return Response(serialize.SerializeDesignation(designation_to_update).data,
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
            return Response({"msg": "Invalid designation"}, status=status.HTTP_400_BAD_REQUEST)

        designation_name = self.queryset[0].title
        self.queryset[0].delete()

        helper.log_activity(request, f"Designation {designation_name} deleted")

        try:
            logs.designation_logger().info(f"{helper.get_user_info(request)} - Designation "
                                           f" {designation_name} deleted")
            return Response({"msg": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def _validate_designation_data(request):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
        if "designation_name" not in request.data:
            return Response({"msg": "Designation name is required"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data["designation_name"].strip() == "":
            return Response({"msg": "Designation name can not be blank"}, status=status.HTTP_400_BAD_REQUEST)
        return "OK"
