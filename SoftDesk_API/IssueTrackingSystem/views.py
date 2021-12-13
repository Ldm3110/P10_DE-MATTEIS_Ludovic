from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from IssueTrackingSystem.models import Projects, Issues, Contributors, Comments
from IssueTrackingSystem.serializers import ProjectSerializer, IssueSerializer, ContributorSerializer, CommentSerializer
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
        return Issues.objects.filter(project_id=self.kwargs['project_pk'])

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
        Create a new Issue and add manually project_id and author_user_id after having retrieved it in the url
        """
        project_instance = self.get_project()
        serializer.save(
            project_id=project_instance,
            author_user_id=self.request.user
        )

    def destroy(self, request, *args, **kwargs):
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
        print("rentre dans get_queryset\n")
        return Comments.objects.filter(
            issues_id__project_id=self.kwargs['project_pk']
        )

    def get_object(self):
        """
        Return instance of the "Issues" object
        """
        print("rentre dans get_object\n")
        try:
            instance = Comments.objects.get(
                issues_id=self.kwargs['issue_pk'],
                id=self.kwargs['pk']
            )
            self.check_object_permissions(self.request, instance)
            return instance
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_issue(self):
        try:
            instance = Issues.objects.get(id=self.kwargs['issue_pk'])
            return instance
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        issue_instance = self.get_issue()
        serializer.save(
            issues_id=issue_instance,
            author_user_id=self.request.user
        )


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributors.objects.filter()
    serializer_class = ContributorSerializer
    permission_classes = [IsProjectCreatorOrContributor]

    def get_object(self):
        try:
            instance = Contributors.objects.get(
                user_id=self.kwargs['pk'],
                project_id=self.kwargs['project_pk']
            )
            return instance
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
