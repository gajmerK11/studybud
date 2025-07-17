from django.urls import path
from . import views

urlpatterns = [
    # path for login
    path('login/', views.loginPage, name="login"),

    # path for logout
    path('logout/', views.logoutUser, name="logout"),
    
    # path for register
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    
    # to make the each value of list 'rooms' clickable and to pass the id to the url we have added '<str:pk>' i.e. we are passing a dynamic value here  
    path('room/<str:pk>/', views.room, name="room"),

    # url for userprofile
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),

    # url for creating room
    path('create-room/', views.createRoom, name="create-room"),
    
    # url for updating room
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),

    # url for deleting room
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),

    # url for deleting message/comment
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    # url for updating user profile
    path('update-user/', views.updateUser, name="update-user"),
    
    path('topics/', views.topicsPage, name="topics"),

    path('activity/', views.activityPage, name="activity"),
]