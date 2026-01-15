from django.urls import path
from . import views

urlpatterns = [
    # Here empty string '' means that it is the root url for this specific url configuration. 
    # In this case, it means that when a user visits the base URL of this app (e.g., /api/), the getRoutes view will be called.
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
]