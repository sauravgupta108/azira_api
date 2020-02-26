from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from azira_bb.api_views import PermissionHandler
from azira_bb import models as az_model

from azira_bb import api_serializers as serialize


class Organization(ModelViewSet):
    serializer_class = serialize.SerializeOrganization
    queryset = az_model.Organization.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        if self.queryset.count() == 0:
            return Response({"msg": "No records found"}, status=status.HTTP_204_NO_CONTENT)

        return Response(serialize.SerializeOrganization(self.queryset, many=True).data,
                        status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        self.queryset = self.queryset.filter(*args, **kwargs)

        if self.queryset.count() != 1:
            return Response({"msg": "Invalid Organization ID"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serialize.SerializeOrganization(self.queryset[0]).data,
                        status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        validity = self._validate_organization_data(request)

        if validity != "OK":
            return validity

        new_org = az_model.Organization.objects.create(name=request.data["org_name"])

        return Response(serialize.SerializeOrganization(new_org).data,
                        status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        validity = self._validate_organization_data(request)

        if validity != "OK":
            return validity

        self.queryset = self.queryset.filter(*args, **kwargs)

        if self.queryset.count != 1:
            return Response({"msg": "Invalid Organization ID"}, status=status.HTTP_400_BAD_REQUEST)

        org_to_update = self.queryset[0]
        org_to_update.title = request.data["org_name"]
        org_to_update.save()

        return Response(serialize.SerializeOrganization(org_to_update).data,
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        self.queryset = self.queryset.filter(*args, **kwargs)

        if self.queryset.count != 1:
            return Response({"msg": "Invalid Organization ID"}, status=status.HTTP_400_BAD_REQUEST)

        self.queryset[0].delete()
        return Response({"msg": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def _validate_organization_data(request):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
        if "org_name" not in request.data:
            return Response({"msg": "Organization name is required"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data["org_name"].strip() == "":
            return Response({"msg": "Organization name can not be blank"}, status=status.HTTP_400_BAD_REQUEST)
        return "OK"
