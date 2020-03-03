from azira_bb import models
from azira_bb.utils import etc_helper as helper


class PermissionHandler:
    def __init__(self, user_id):
        self.user = None
        try:
            self.user = models.AzUser.objects.get(user_id=user_id)
        except (models.AzUser.DoesNotExist, models.AzUser.MultipleObjectsReturned):
            helper.log_message(f"Invalid user_id <{user_id}>", log_type="error")

    def can_create_or_update_project(self):
        return True if self.is_super_user() else False

    def can_create_sprint(self, project_id):
        if self.is_super_user():
            return True
        return self.is_project_owner(project_id)

    def get_az_user(self):
        return self.user

    def is_super_user(self):
        if self.user and self.user.is_admin:
            return True
        return False

    def is_project_owner(self, project_id):
        try:
            project_owner = models.Project.objects.get(project_id=project_id).get_project_owner()
            if self.user and (self.user.id == project_owner.user.id):
                return True
        except (models.Project.DoesNotExist, models.Project.MultipleObjectsReturned):
            helper.log_message(f"Invalid project id <{project_id}>", log_type="error")
            return False
        return False

    def is_team_manager(self, team_id):
        try:
            team = models.Team.objects.get(id=int(team_id))
            return team.manager.id == self.user.id
        except (models.Team.DoesNotExist, models.Team.MultipleObjectsReturned, ValueError):
            helper.log_message(f"Invalid team id <{self.user.id}>", log_type="error")
            return False

    def is_team_lead(self, team_id):
        try:
            team = models.Team.objects.get(id=int(team_id))
            return team.lead_id == self.user.id
        except (models.Team.DoesNotExist, models.Team.MultipleObjectsReturned, ValueError):
            helper.log_message(f"Invalid team id <{self.user.id}>", log_type="error")
            return False

    def is_team_member(self, team_id):
        try:
            team = models.Team.objects.get(id=int(team_id))
            return self.user.id in team.members.all().values_list("id", flat=True)
        except (models.Team.DoesNotExist, models.Team.MultipleObjectsReturned, ValueError):
            helper.log_message(f"Invalid team id <{self.user.id}>", log_type="error")
            return False

    def can_create_team(self, project_id):
        try:
            project = models.Project.objects.get(id=int(project_id))
            return self.user and project.get_project_owner().user.id == self.user.id
        except (ValueError, models.Project.DoesNotExist, models.Project.MultipleObjectsReturned):
            helper.log_message(f"Invalid project id <{project_id}>", log_type="error")
            return False

    def can_modify_team(self, team_id):
        return self.is_team_member(team_id)

    def can_view_team(self, team_id):
        return self.is_super_user() or self.is_team_member(team_id) or self.is_team_manager(team_id) or \
               self.is_team_lead(team_id)
