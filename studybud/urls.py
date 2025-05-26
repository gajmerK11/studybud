from django.contrib import admin
from django.urls import path
from django.http import HttpResponse


def home(request):
    # when this function will be triggered, it will return a http response that will return a string saying "Home page"
    return HttpResponse("Home page")

# anoter route
# our website is going to have rooms for different conversations so we are creating a route for it
def room(request):
    return HttpResponse("ROOM")

urlpatterns = [
    path('admin/', admin.site.urls),
    # what the below code is saying is: when someone goes to home page (empty string '' here represents home page), we are going to send that user to home (which is the function we created above that returns http response with a string saying "Home page").
    path('', home),
    path('room/',room)
]
