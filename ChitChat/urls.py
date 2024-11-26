from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('create/', views.create_private_group, name='create_group'),
    path('<slug:slug>/', views.room, name='room'),
]