from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    client_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_clients')

    def __str__(self):
        return str(self.client_name)


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    users = models.ManyToManyField(
        User, related_name='projects_assigned', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_projects', null=True, blank=True)

    def __str__(self):
        return str(self.project_name)
