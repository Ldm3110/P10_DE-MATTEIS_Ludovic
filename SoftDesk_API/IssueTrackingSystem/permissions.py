from rest_framework.permissions import BasePermission

from IssueTrackingSystem.models import Contributors, Issues


class IsProjectCreatorOrContributor(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            try:
                contribution = request.user.contributors_set.get(project_id=obj.id)
                if contribution.role == "CREATEUR" or contribution.role == "CONTRIBUTEUR":
                    return True
            except Contributors.DoesNotExist:
                return False

        elif request.method in {"PUT", "DELETE"}:
            try:
                contribution = request.user.contributors_set.get(project_id=obj.id)
                if contribution.role == "CREATEUR":
                    return True
            except Contributors.DoesNotExist:
                return False


class IsIssueAuthor(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in {"GET", "POST"}:
            try:
                contribution = request.user.contributors_set.get(project_id=obj.project_id)
                if contribution.role == "CREATEUR" or contribution.role == "CONTRIBUTEUR":
                    return True
            except Contributors.DoesNotExist:
                return False

        elif request.method in {"PUT", "DELETE"}:
            return request.user == obj.author_user_id


class IsCommentAuthor(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == {"GET", "POST"}:
            try:
                issue = Issues.objects.get(id=obj.issues_id_id)
                contribution = request.user.contributors_set.get(project_id=issue.project_id)
                if contribution.role == "CREATEUR" or contribution.role == "CONTRIBUTEUR":
                    return True
            except Contributors.DoesNotExist:
                return False

        elif request.method in {"PUT", "DELETE"}:
            return request.user == obj.author_user_id
