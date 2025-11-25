from django.urls import path
from . import views

urlpatterns = [
    # General
    path('', views.home, name='home'),
    # Client
    path('create-client/', views.create_client, name='create_client'),
    path('client_list/', views.client_list, name='client_list'),
]