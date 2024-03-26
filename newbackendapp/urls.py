from django.urls import path

from newbackendapp import views

app_name = "newbackendapp"

urlpatterns = [
    path('clients/', views.get_clients, name='get_clients'),
    path("clients/<int:pk>/", views.client_api, name="client_api"),
    path("projects/", views.get_project, name="get_project"),
    path('projects/<int:pk>/', views.delete_project_api,
         name='delete_project_api'),
]
