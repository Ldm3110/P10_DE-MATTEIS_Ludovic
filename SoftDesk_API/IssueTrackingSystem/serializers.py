from rest_framework import serializers

from IssueTrackingSystem.models import Projects, Issues, Comments, Contributors


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = [
            'user_id',
            'project_id',
            'role'
        ]
        extra_kwargs = {
            'role': {'default': 'CONTRIBUTEUR'}
        }
