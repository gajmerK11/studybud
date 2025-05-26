from django.shortcuts import render

# Create your views here.
def home(request):
    # when this function will be triggered, it will render 'home.html' file
    # render function takes 2 parameters: first one 'request' object, second one 'template' that we want to render
    return render(request, 'home.html')

# anoter route
# our website is going to have rooms for different conversations so we are creating a route for it
def room(request):
    return render(request, 'room.html')