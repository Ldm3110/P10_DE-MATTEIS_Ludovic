from rest_framework import serializers

from IssueTrackingSystem.models import Projects, Issues, Comments, Contributors


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = [
            'id',
            'title',
            'description',
            'type'
        ]


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = [
            'id',
            'title',
            'description',
            'tag',
            'priority',
            'status'
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['description']


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = [
            'user_id',
            'role'
        ]
        extra_kwargs = {
            'role': {'default': 'CONTRIBUTEUR'}
        }
