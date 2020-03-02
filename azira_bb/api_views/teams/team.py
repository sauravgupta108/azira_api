from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from azira_bb import models as az_models
from azira_bb.api_views import PermissionHandler


class NewTeam(APIView):
    def get(self, request):
        pass
