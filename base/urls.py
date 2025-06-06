from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
    # to make the each value of list 'rooms' clickable and to pass the id to the url we have added '<str:pk>' i.e. we are passing a dynamic value here  
    path('room/<str:pk>/', views.room, name="room"),

    path('create-room/', views.createRoom, name="create-room"),
]