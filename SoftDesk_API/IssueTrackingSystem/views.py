from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from IssueTrackingSystem.models import Projects, Issues, Contributors
from IssueTrackingSystem.serializers import ProjectSerializer, IssueSerializer, ContributorSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Projects.objects.filter()

    def perform_create(self, serializer):
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
    permission_classes = [IsAuthenticated]

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

