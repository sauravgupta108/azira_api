from azira_bb import models
from azira_bb.utils.etc_helper import log_message


class PermissionHandler:
    def __init__(self, user_id):
        self.user = None
        try:
            self.user = models.AzUser.objects.get(user_id=user_id)
        except (models.AzUser.DoesNotExist, models.AzUser.MultipleObjectsReturned):
            log_message(f"Invalid user_id <{user_id}>", log_type="error")

    def can_create_project(self):
        return True if self.is_super_user() else False

    def can_create_sprint(self, project_id):
        if self.is_super_user():
            return True
        return self.is_project_owner(project_id)

    def can_create_issue(self, sprint_id):
        if self.is_super_user():
            return True
        team = self.get_team(sprint_id)
        if not team:
            return False
        return self.is_team_lead(team) and self.is_team_manager(team)

    def can_comment(self, issue_id):
        if self.is_super_user():
            return True
        try:
            issue = models.Issue.objects.get(id=issue_id)
        except (models.Issue.DoesNotExist, models.Issue.MultipleObjectsReturned):
            log_message(f"Invalid issue id <{issue_id}>", log_type="error")
            return False
        team = self.get_team(issue.sprint_id)
        if not team:
            return False

        return self.is_team_lead(team) and self.is_team_manager(team) and self.is_team_member(team)

    @staticmethod
    def get_team(sprint_id):
        try:
            team = models.Team.objects.get(sprint_id=sprint_id)
        except (models.Team.DoesNotExist, models.Team.MultipleObjectsReturned):
            log_message(f"Invalid sprint id <{sprint_id}>", log_type="error")
            return None
        return team

    def is_super_user(self):
        if self.user and self.user.is_admin:
            return True
        return False

    def is_project_owner(self, project_id):
        try:
            project_owner = models.ProjectAccess.objects.get(project_id=project_id).owner
            if self.user and (self.user.id == project_owner.user.id):
                return True
        except (models.ProjectAccess.DoesNotExist, models.ProjectAccess.MultipleObjectsReturned):
            log_message(f"Invalid project id <{project_id}>", log_type="error")
            return False
        return False

    def is_team_manager(self, team):
        return True if self.user and (self.user.id == team.manager.user.id) else False

    def is_team_lead(self, team):
        return True if self.user and (self.user.id == team.lead.user.id) else False

    def is_team_member(self, team):
        return True if self.user and (self.user.id in team.members.all().values_list("user_id", flat=True)) else False
