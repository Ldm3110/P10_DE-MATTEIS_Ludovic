from rest_framework.permissions import BasePermission

from IssueTrackingSystem.models import Contributors


class IsProjectCreatorOrContributor(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            try:
                contribution = request.user.contributors_set.get(project_id=obj.project_id)
                if contribution.role == "CREATEUR" or contribution.role == "CONTRIBUTEUR":
                    return True
            except Contributors.DoesNotExist:
                return False

        elif request.method in {"PUT", "DELETE"}:
            try:
                contribution = request.user.contributors_set.get(project_id=obj.project_id)
                if contribution.role == "CREATEUR":
                    return True
            except Contributors.DoesNotExist:
                return False


class IsIssueOrCommentAuthor(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            try:
                contribution = request.user.contributors_set.get(project_id=obj.project_id)
                if contribution.role == "CREATEUR" or contribution.role == "CONTRIBUTEUR":
                    return True
            except Contributors.DoesNotExist:
                return False

        elif request.method in {"PUT", "DELETE"}:
            return request.user == obj.author_user_id
