from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils.dateparse import parse_date

from azira_bb import models as az_models
from azira_bb import api_serializers as serialize
from azira_bb.utils import etc_helper as helper
from azira_bb.api_views import PermissionHandler
from azira_bb.utils import options
from azira_bb.utils import loggers as logs


def get_project_details(request, project_id):
    try:
        if not request.user.id:
            return None

        project = az_models.Project.objects.get(id=int(project_id))
        project_details = serialize.SerializeProjectDetailed(project)

        return project_details

    except (az_models.Project.DoesNotExist, az_models.Project.MultipleObjectsReturned, ValueError):
        logs.project_logger().error("Invalid project ID", exc_info=True)
        return None
    except AttributeError:
        logs.project_logger().error("Invalid request", exc_info=True)
        return None


class Project(ModelViewSet):
    queryset = az_models.Project.objects.all()
    serializer_class = serialize.SerializeProjectConcise
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        if self.queryset.count() == 0:
            return Response({"msg": "No projects found"}, status=status.HTTP_204_NO_CONTENT)

        try:
            logs.project_logger().info(f"{helper.get_user_info(request)} | Project's List")

            return Response(serialize.SerializeProjectConcise(self.queryset).data,
                            status=status.HTTP_200_OK)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        project_details = get_project_details(request, kwargs["pk"])
        if not project_details:
            return Response({"msg": "Invalid project ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            logs.project_logger().info(f"{helper.get_user_info(request)} | Project | {project_details['id']} "
                                       f"| {project_details['name']}")

            return Response(project_details, status=status.HTTP_200_OK)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        request_validity = self._validate_project_request(request)
        if request_validity != "OK":
            return request_validity

        try:
            start_date, end_date = self._get_start_or_end_date(request)
        except ValueError as error:
            return Response({"msg": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                new_project = az_models.Project()
                new_project.name = request.data["proj_name"].strip()
                new_project.start_date = start_date

                if end_date:
                    new_project.end_date = end_date

                new_project.save()

                helper.log_activity(request, f"New project '{new_project.name}' created")

                logs.project_logger().info(f"{helper.get_user_info(request)} | Project | {new_project.id} "
                                           f"| {new_project.name} created")

                return Response(get_project_details(request, new_project.id),
                                status=status.HTTP_201_CREATED)

        except ValueError as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Error ({str(error)})"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Error ({str(error)})"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        request_validity = self._validate_project_request(request)
        if request_validity != "OK":
            return request_validity

        self.queryset = self.queryset.filter(*args, **kwargs)
        if self.queryset.count() != 1:
            return Response({"msg": "Invalid Project ID"}, status=status.HTTP_400_BAD_REQUEST)

        project_to_update = self.queryset[0]

        try:
            start_date, end_date = self._get_start_or_end_date(request)
        except ValueError as error:
            return Response({"msg": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                project_to_update.name = request.data["proj_name"].strip()
                project_to_update.start_date = start_date

                if end_date:
                    project_to_update.end_date = end_date

                project_to_update.save()

                helper.log_activity(request, f"Project with id {project_to_update.id} updated")

                logs.project_logger().info(f"{helper.get_user_info(request)} | Project | {project_to_update.id} "
                                           f"| {project_to_update.name} updated")

                return Response(get_project_details(request, project_to_update.id),
                                status=status.HTTP_200_OK)

        except ValueError as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Error ({str(error)})"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Error ({str(error)})"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).can_create_or_update_project():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"msg": "Not Implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        if not PermissionHandler(request.user.id).can_create_or_update_project():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        self.queryset = self.queryset.filter(*args, **kwargs)
        if self.queryset.count() != 1:
            return Response({"msg": "Invalid Project ID"}, status=status.HTTP_400_BAD_REQUEST)

        project_to_delete = self.queryset[0]
        project_id, name = project_to_delete.id, project_to_delete.name

        project_to_delete.delete()

        helper.log_activity(request, f"Project deleted. ID: {project_id}, Name: {name}")

        try:
            logs.project_logger().info(f"{helper.get_user_info(request)} | Project | {project_id} "
                                       f"| {name}")

            return Response({"msg": f"Project {name} deleted successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def _validate_project_request(request):
        if not PermissionHandler(request.user.id).can_create_or_update_project():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        if "proj_name" not in request.data:
            return Response({"msg": "Project Name is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data["proj_name"].strip() == "":
                return Response({"msg": "Project Name can not be blank"},
                                status=status.HTTP_400_BAD_REQUEST)

        if "start_date" not in request.data:
            return Response({"msg": "Start date is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data["start_date"].strip() == "":
                return Response({"msg": "Start date can not be blank"},
                                status=status.HTTP_400_BAD_REQUEST)
        return "OK"

    @staticmethod
    def _get_start_or_end_date(request):
        start_date = parse_date(request.data["start_date"].strip())
        if not start_date:
            raise ValueError("Invalid start date format. Valid format is YYYY-MM-DD")

        end_date = None
        if "end_date" in request.data:
            end_date = parse_date(request.data["end_date"].strip())
            if not end_date:
                raise ValueError("Invalid end date format. Valid format is YYYY-MM-DD")
        return start_date, end_date


class ProjectAccess(APIView):
    @staticmethod
    def get(request):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        all_projects = az_models.Project.objects.all()
        serialized_projects = serialize.SerializeProjectMicro(all_projects, many=True).data

        all_users = az_models.AzUser.objects.filter(designation__code=options.TEAM_MANAGER)
        serialized_users = serialize.SerializeUserProjectAccess(all_users, many=True).data

        try:
            logs.project_logger().info(f"{helper.get_user_info(request)} | Project's List for Access")
            response = {"projects": serialized_projects, "users": serialized_users}
            return Response(response, status=status.HTTP_200_OK)

        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def post(request):
        if not PermissionHandler(request.user.id).is_super_user():
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        if "project" not in request.data:
            return Response({"msg": "Project is required"}, status=status.HTTP_400_BAD_REQUEST)

        if "user" not in request.data:
            return Response({"msg": "User is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = az_models.Project.objects.get(id=int(request.data["project"]))
        except (ValueError, az_models.Project.DoesNotExist, az_models.Project.MultipleObjectsReturned):
            return Response({"msg": "Invalid project"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            owner = az_models.AzUser.objects.get(id=int(request.data["user"]),
                                                 designation__code=options.TEAM_MANAGER)
        except (ValueError, az_models.AzUser.DoesNotExist, az_models.AzUser.MultipleObjectsReturned):
            return Response({"msg": "Invalid project"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_project_access = az_models.ProjectAccess.objects.create(project=project, owner=owner)
            helper.log_activity(f"New Project Access created. id: {new_project_access.id}", "error")
            logs.project_logger().info(f"{helper.get_user_info(request)} | Project Access granted for | "
                                       f"{new_project_access.project.name} | to |"
                                       f"{new_project_access.owner.user.get_full_name()}")
            return Response(serialize.SerializeUserProjectAccess(new_project_access),
                            status=status.HTTP_201_CREATED)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Error ({str(error)})"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
