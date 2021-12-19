from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response

from IssueTrackingSystem.models import Projects, Issues, Contributors, Comments
from IssueTrackingSystem.serializers import ProjectSerializer, IssueSerializer, ContributorSerializer, \
    CommentSerializer
from IssueTrackingSystem.permissions import IsProjectCreatorOrContributor, IsIssueAuthor, IsCommentAuthor


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    # Permissions OK pour toutes les actions propres à un projet
    permission_classes = [IsProjectCreatorOrContributor, ]

    def get_queryset(self):
        return Projects.objects.filter()

    def list(self, request, *args, **kwargs):
        """
        Return all the Projects which user in "CREATEUR" or "CONTRIBUTEUR"
        """
        projects = request.user.projects_set.all()
        serialized_project = ProjectSerializer(projects, many=True)
        return Response(serialized_project.data)

    def perform_create(self, serializer):
        """
        Create a new project and add a new instance of contributors in Contributors class with the role "CREATEUR"
        """
        project = serializer.save()
        Contributors.objects.create(
            user_id=self.request.user,
            project_id=project,
            role='CREATEUR'
        )


class IssuesViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsIssueAuthor, ]

    def get_queryset(self):
        """
        1. Check if the user has the autorisation to see issues
        2. If the user has permission -> return issues
        """
        issues = Issues.objects.filter(project_id=self.kwargs['project_pk'])
        for issue in issues:
            self.check_object_permissions(self.request, issue)
        return issues

    def get_object(self):
        """
        Return instance of the "Issues" object
        """
        try:
            instance = Issues.objects.get(
                project_id=self.kwargs['project_pk'],
                id=self.kwargs['pk']
            )
            self.check_object_permissions(self.request, instance)
            return instance
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        """
        1. Check if the user has authorisation to create an issue
        2. Extract the instance of the project to have the project_id
        3. Create a new Issue and add manually project_id and author_user_id after having retrieved it in the url
        """
        self.get_queryset()
        try:
            project_instance = Projects.objects.get(id=self.kwargs['project_pk'])
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer.save(
            project_id=project_instance,
            author_user_id=self.request.user
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific issue
        """
        try:
            instance = self.get_object()
            self.check_object_permissions(request, instance)
            self.perform_destroy(instance)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthor, ]

    def get_queryset(self):
        """
        1. Check if the user has the autorisation to see comments
        2. If the user has permission -> return issues
        """
        comments = Comments.objects.filter(
            issues_id__project_id=self.kwargs['project_pk']
        )
        for comment in comments:
            self.check_object_permissions(self.request, comment)
        return comments

    def get_object(self):
        """
        Return instance of the "Issues" object
        """
        try:
            instance = Comments.objects.get(
                issues_id=self.kwargs['issue_pk'],
                id=self.kwargs['pk']
            )
            self.check_object_permissions(self.request, instance)
            return instance
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        """
        1. Check if the user has the permission to create a comment
        2. Extract the instance of the comment to have the issue_id
        3. Create the comment
        """
        self.get_queryset()
        try:
            instance = Issues.objects.get(id=self.kwargs['issue_pk'])
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer.save(
            issues_id=instance,
            author_user_id=self.request.user
        )


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsProjectCreatorOrContributor]

    def get_queryset(self):
        return Contributors.objects.filter(project_id=self.kwargs['project_pk'])

    def get_object(self):
        """
        Return the instance of a Contributor
        """
        try:
            instance = Contributors.objects.get(
                user_id=self.kwargs['pk'],
                project_id=self.kwargs['project_pk']
            )
            return instance
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_project(self):
        """
        Find instance of the "Projects" object and send it back for creation
        """
        try:
            instance = Projects.objects.get(id=self.kwargs['project_pk'])
            return instance
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        """
        Create a new Contributor and add manually project_id and author_user_id after having retrieved it in the url
        """
        project_instance = self.get_project()
        try:
            # Try to find this Contributor to avoid creating a duplicate
            Contributors.objects.get(
                project_id=project_instance,
                user_id=self.request.POST.get("user_id")
            )
        except Contributors.DoesNotExist:
            # Contributor does not exist -- Creation of the Contributor
            serializer.save(
                project_id=project_instance,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a contributor of a project
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Contributors.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
