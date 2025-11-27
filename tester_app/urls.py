from django.urls import path
from . import views

urlpatterns = [
    # General
    path('', views.home, name='home'),
    # Proposal
    path('proposal/<int:pk>/update', views.update_proposal, name='update_proposal'),
    path('create-proposal/', views.create_proposal, name='create_proposal'),
    path('proposal-list/', views.proposal_list, name='proposal_list'),
    # Client
    path('wilayah/<path:endpoint>', views.wilayah_proxy, name='wilayah_proxy'),
    path('create-client/', views.create_client, name='create_client'),
    path('client-list/', views.client_list, name='client_list'),
    path('client/<int:pk>/update', views.update_client, name='update_client'),
    path('client/<int:pk>/delete/', views.delete_client, name='delete_client'),
]