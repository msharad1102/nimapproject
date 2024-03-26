from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project


class AllProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "project_name", "created_at",
                  "created_by", "client_name"]

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None

    def get_client_name(self, obj):
        if obj.client:
            return obj.client.client_name
        return None


class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'created_by', 'project_name',
                  'created_at', 'client', 'users']
        read_only_fields = ['id', 'created_at']

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None

    def get_client(self, obj):
        if obj.client:
            return obj.client.client_name
        return None


class ClientPullListSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ["id", "client_name", "created_at", "created_by"]

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class NewProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'project_name']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        client_id = self.context['view'].kwargs.get('client_id')
        client = Client.objects.get(pk=client_id)
        users_data = validated_data.pop('users', [])
        project = Project.objects.create(client=client, **validated_data)
        project.users.set(users_data)
        return project


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class ClientListSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    projects = NewProjectSerializer(
        many=True, read_only=True, source='projects.all')

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects',
                  'created_at', 'created_by', 'updated_at']

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class NewClientListSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at',
                  'created_by', 'updated_at']

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None

