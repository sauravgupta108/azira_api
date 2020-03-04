from uuid import uuid4

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from azira_bb import models as az_model
from azira_bb import api_serializers as serialize
from azira_bb.utils import etc_helper as helper
from azira_bb.utils import loggers as logs


class AziraLogin(APIView):

    @staticmethod
    def post(request):
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(username=username, password=password)

        if not user:
            logs.user_logger().info(f"Invalid login attempt with username <{username}>")
            return Response({"msg": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        user_token = Token.objects.filter(user=user).first()

        try:
            az_user = az_model.AzUser.objects.get(user_id=user.id)
        except (az_model.AzUser.DoesNotExist, az_model.AzUser.MultipleObjectsReturned):
            logs.super_logger().error(f"Problem with user of username <{username}>", exc_info=True)
            helper.log_message(f"Problem with user of username <{username}>", log_type="error")
            return Response({"msg": "Internal Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not user_token:
            user_token = Token.objects.create(key=str(uuid4()), user=user)
            logs.user_logger().info(f"New token created for user {user.get_full_name()}")

        user_details = serialize.SerializeLoggedInUser(az_user).data
        user_details["Token"] = user_token.key

        return Response(user_details, status=status.HTTP_200_OK)
