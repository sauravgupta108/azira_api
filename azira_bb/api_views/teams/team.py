from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from azira_bb import models as az_models
from azira_bb.api_views import PermissionHandler
from azira_bb.utils import options
from azira_bb.utils import etc_helper as helper
from azira_bb.utils import loggers as logs
from azira_bb.api_serializers import UserSerializerMicro
from azira_bb.api_serializers import SerializeTeamMicro, SerializeTeamDetailed
from azira_bb.api_serializers import SerializeSprintMicro, SerializeProjectMicro


class NewTeam(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        if "project_id" not in request.query_params:
            return Response({"msg": "Project id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not PermissionHandler(request.user.id).can_create_team(request.query_params["project_id"]):
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        team_members = az_models.AzUser.objects.filter(designation__code=options.TEAM_MEMBER
                                                       ).values_list("user", flat=True)
        team_leads = az_models.AzUser.objects.filter(designation__code=options.TEAM_LEAD
                                                     ).values_list("user", flat=True)

        project = az_models.Project.objects.get(id=int(request.query_params["project_id"]))
        sprints = SerializeSprintMicro(project.get_sprints(), many=True).data

        team_members_details = UserSerializerMicro(team_members, many=True).data
        team_leads_details = UserSerializerMicro(team_leads, many=True).data

        response = {"project": SerializeProjectMicro(project).data, "sprints": sprints,
                    "team_leads": team_leads_details, "team_members": team_members_details}

        return Response(response, status=status.HTTP_200_OK)


class TeamSet(ModelViewSet, PermissionHandler):
    queryset = az_models.Team.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        permission_obj = PermissionHandler(request.user.id)

        try:
            logs.team_logger().info(f"{helper.get_user_info(request)} - Team's List")

            if permission_obj.is_super_user():
                all_teams = SerializeTeamMicro(self.queryset, many=True).data
                return Response(all_teams, status=status.HTTP_200_OK)

            elif permission_obj.user.designation.code == options.TEAM_MANAGER:
                teams = self.queryset.filter(manager=permission_obj.user)
                all_teams_owned = SerializeTeamMicro(teams, many=True).data
                return Response(all_teams_owned, status=status.HTTP_200_OK)

            elif permission_obj.user.designation.code == options.TEAM_LEAD:
                teams = self.queryset.filter(lead=permission_obj.user)
                teams_owned = SerializeTeamMicro(teams, many=True).data
                return Response(teams_owned, status=status.HTTP_200_OK)

            else:
                return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):

        self.queryset = self.queryset.filter(*args, **kwargs)

        if self.queryset.count() != 1:
            return Response({"msg": "No Team found"}, status=status.HTTP_204_NO_CONTENT)

        team = self.queryset[0]

        try:
            if PermissionHandler(request.user.id).can_view_team(team.id):
                logs.team_logger().info(f"{helper.get_user_info(request)} - Team | {team.id} | {team.name}")
                return Response(SerializeTeamDetailed(team).data, status=status.HTTP_200_OK)
            else:
                logs.team_logger().info(f"{helper.get_user_info(request)} - Unauthorized access to team")
                return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Server Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        if "project_id" not in request.data:
            return Response({"msg": "Project is required"}, status=status.HTTP_400_BAD_REQUEST)

        permission_obj = PermissionHandler(request.user.id)

        # Validating Team Name
        if "team_name" not in request.data:
            return Response({"msg": "Team name is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data["team_name"].strip() == "":
                return Response({"msg": "Team name can not be blank"}, status=status.HTTP_400_BAD_REQUEST)

        # Validating Project
        if not permission_obj.can_create_team(request.data["project_id"]):
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
        else:
            try:
                project = az_models.Project.objects.get(id=int(request.data["project_id"]))
            except (ValueError, az_models.Project.DoesNotExist, az_models.Project.MultipleObjectsReturned):
                return Response({"msg": "Invalid Project ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Validating Sprint
        if "sprint_id" not in request.data:
            return Response({"msg": "Sprint is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                project_sprints = project.get_sprints()
                if int(request.data["sprint_id"]) not in project_sprints.values_list("id", flat=True):
                    raise ValueError

                sprint = project_sprints.filter(id=int(request.data["sprint_id"]))[0]
            except (ValueError, IndexError):
                return Response({"msg": "Invalid Sprint ID"}, status=status.HTTP_400_BAD_REQUEST)

        if "team_lead_id" not in request.data:
            return Response({"msg": "Team Lead is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                lead = az_models.AzUser.objects.get(id=int(request.daat["team_lead_id"]),
                                                    designation__code=options.TEAM_LEAD)
            except (ValueError, az_models.AzUser.DoesNotExist, az_models.AzUser.MultipleObjectsReturned):
                return Response({"msg": "Invalid Team Lead"}, status=status.HTTP_400_BAD_REQUEST)

        if "team_members" not in request.data:
            return Response({"msg": "Team Members are required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            team_members_id = request.data["team_members"].split(",")

            if len(team_members_id) == 0:
                return Response({"msg": "Team Members are required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                team_members_ids = list(map(int, team_members_id))
                team_members = list()

                for team_member_id in team_members_ids:
                    member = az_models.AzUser.objects.get(id=team_member_id, designation__code=options.TEAM_MEMBER)
                    team_members.append(member)

                if len(team_members) == 0:
                    raise ValueError
            except (ValueError, az_models.AzUser.DoesNotExist, az_models.AzUser.MultipleObjectsReturned):
                return Response({"msg": "Invalid Team Member(s)"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                new_team = az_models.Team()

                new_team.name = request.data["team_name"]
                new_team.project = project
                new_team.sprint = sprint
                new_team.lead = lead
                new_team.manager = permission_obj.user
                new_team.save()

                new_team.members.add(*team_members)
                new_team.save()

                helper.log_activity(request, f"New Team | {new_team.id} | {new_team.name} | created")
                logs.team_logger().info(f"{helper.get_user_info(request)}: New Team | {new_team.id} | "
                                        f"{new_team.name} | created")
                return Response(SerializeTeamDetailed(new_team).data, status=status.HTTP_201_CREATED)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Error {str(error)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        return Response({"msg": "Not Implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    def partial_update(self, request, *args, **kwargs):
        permission_obj = PermissionHandler(request.user.id)
        if not permission_obj.can_modify_team(request.data["project_id"]):
            return Response({"msg": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        self.queryset = self.queryset.filter(*args, **kwargs)
        if len(self.queryset) != 1:
            return Response({"msg": "Invalid Team"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            team = self.queryset[0]

            if "team_name" in request.data:
                if request.data["team_name"].strip() == "":
                    return Response({"msg": "Team Name can not be blank"}, status=status.HTTP_400_BAD_REQUEST)
                older_name = team.name
                team.name = request.data["team_name"]
                team.save()

                helper.log_activity(request, f"Team name changed from {older_name} to {team.name}")
                logs.team_logger().info(f"{helper.get_user_info(request)}: Team {team.id} | {older_name} | "
                                        f"name changed to {team.name}")

            if "team_lead" in request.data:
                try:
                    new_lead = az_models.AzUser.objects.get(id=int(request.data["team_lead"]),
                                                            designation__code=options.TEAM_LEAD)
                    older_lead = team.lead.user.get_full_name()
                    team.lead = new_lead
                    team.save()
                    new_lead_name = team.lead.user.get_full_name()

                    helper.log_activity(request, f"Team lead changed from {older_lead} to {new_lead_name} of team "
                                                 f"{team.name}")
                    logs.team_logger().info(f"{helper.get_user_info(request)}: Team {team.id} | {team.name} | "
                                            f"lead changed to {new_lead_name} from {older_lead}")

                except (ValueError, az_models.AzUser.DoesNotExist, az_models.AzUser.MultipleObjectsReturned):
                    logs.super_logger().error(f"Invalid Team Lead", exc_info=True)
                    return Response({"msg": "Invalid Team Lead"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(SerializeTeamDetailed(team).data, status=status.HTTP_200_OK)
        except Exception as error:
            logs.super_logger().error(f"Internal Error", exc_info=True)
            return Response({"msg": f"Internal Error {str(error)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        return Response({"msg": "Not Implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)
