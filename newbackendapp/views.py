from django.shortcuts import get_object_or_404
from .models import Client, Project
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


@api_view(["POST", "GET"])
def get_clients(request):
    o_client = Client.objects.all()
    s_client = ClientPullListSerializer(o_client, many=True)

    if request.method == "POST":
        o_user = User.objects.get(id=request.user.id)
        s_client = ProfileSerializer(data=request.data)
        if s_client.is_valid():
            s_client.save()
            print(s_client.data['id'])
            o_client = Client.objects.get(id=s_client.data['id'])
            o_client.created_by = o_user
            o_client.save()
            s_profile = NewClientListSerializer(o_client)
            return Response(s_profile.data)
        return Response(s_client.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(s_client.data)


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def client_api(request, pk):
    try:
        o_candidate = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        s_client = NewClientListSerializer(o_candidate, data=request.data)
        if s_client.is_valid():
            s_client.save()
            return Response(s_client.data)
        return Response(s_client.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        o_candidate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    s_client = ClientListSerializer(o_candidate)
    return Response(s_client.data)


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def get_project(request):
    if request.method == "POST":
        try:
            print(request.POST)
            s_project = ProjectSerializer(data=request.data)
            if s_project.is_valid():
                s_project.save()
                print(s_project.data)
                project = get_object_or_404(Project, pk=s_project.data['id'])
                users = User.objects.filter(pk__in=request.data["users"])
                client = Client.objects.get(id=request.data["client"])
                project.client = client
                project.users.add(*users)
                project.created_by = request.user
                project.save()
                s_project = ProjectSerializer(project)
                return Response(s_project.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            status
            return Response(s_project.errors, status=status.HTTP_400_BAD_REQUEST)

    o_project = Project.objects.all()
    s_project = AllProjectSerializer(o_project, many=True)
    return Response(s_project.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_project_api(request, pk):
    try:
        o_project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        o_project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
