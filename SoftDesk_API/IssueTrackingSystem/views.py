from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from IssueTrackingSystem.models import Projects, Issues, Contributors, Comments
from IssueTrackingSystem.serializers import ProjectSerializer, IssueSerializer, ContributorSerializer, CommentSerializer
from IssueTrackingSystem.permissions import IsProjectCreatorOrContributor


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
        Create a new project and add a new instance of contributors in Contributors class with the role"CREATEUR"
        """
        project = serializer.save()
        Contributors.objects.create(
            user_id=self.request.user,
            project_id=project,
            role='CREATEUR'
        )


class IssuesViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Issues.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        issue = serializer.save()


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

