from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-room/', views.create_room, name='create_room'), 
    path('<slug:slug>/', views.chatroom, name='chatroom'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('delete-room/<slug:slug>/', views.delete_room, name='delete_room'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),    
]
