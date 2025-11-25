from django.urls import path
from . import views

urlpatterns = [
    # General
    path('', views.home, name='home'),
    # Client
    path('wilayah/<path:endpoint>', views.wilayah_proxy, name='wilayah_proxy'),
    path('create-client/', views.create_client, name='create_client'),
    path('client_list/', views.client_list, name='client_list'),
]