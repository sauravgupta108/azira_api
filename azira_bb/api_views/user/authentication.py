from uuid import uuid4

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from azira_bb.utils.etc_helper import log_message
from azira_bb import models as az_model
from azira_bb import api_serializers as serialize


class AziraLogin(APIView):

    @staticmethod
    def post(request):
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(username=username, password=password)

        if not user:
            log_message(f"Invalid login attempt with username <{username}>", log_type="info")
            return Response({"msg": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        user_token = Token.objects.filter(user=user).first()

        try:
            az_user = az_model.AzUser.objects.get(user_id=user.id)
        except (az_model.AzUser.DoesNotExist, az_model.AzUser.MultipleObjectsReturned):
            log_message(f"Problem with user of username <{username}>", log_type="error")
            return Response({"msg": "Internal Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not user_token:
            user_token = Token.objects.create(key=str(uuid4()), user=user)

        user_details = serialize.SerializeLoggedInUser(az_user).data
        user_details["Token"] = user_token.key

        return Response(user_details, status=status.HTTP_200_OK)
