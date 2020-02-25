from azira_bb.models import ProjectAccess
from azira_bb.models import Team
from azira_bb.utils.etc_helper import log_message


class PermissionHandler:
    def __init__(self, user):
        self.user = user

    def can_create_project(self):
        if self.is_super_user():
            return True
        return False

    def can_create_sprint(self, project):
        if self.is_super_user():
            return True
        try:
            project_owner = ProjectAccess.objects.get(project=project).owner
            if self.user.id == project_owner.user.id:
                return True
        except (ProjectAccess.DoesNotExist, ProjectAccess.MultipleObjectsReturned) as error:
            log_message(str(error), log_type="error")
            return False
        return False

    def can_create_issue(self, sprint):
        if self.is_super_user():
            return True
        try:
            team = Team.objects.get(sprint=sprint)
            if self.user.id in [team.lead.user.id, team.manager.user.id]:
                return True
        except (Team.DoesNotExist, Team.MultipleObjectsReturned) as error:
            log_message(str(error), log_type="error")
            return False
        return False

    def is_super_user(self):
        if self.user.is_admin:
            return True
        return False
