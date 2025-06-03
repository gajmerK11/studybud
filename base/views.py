from django.shortcuts import render
from .models import Room

# Create your views here.
# we have created this 'rooms' list of dictionaries to pass data
rooms = [
    {'id': 1, 'name': 'Lets learn python!'},
    {'id': 2, 'name': 'Design with me'},
    {'id': 3, 'name': 'Frontend developers'},
]


def home(request):
    # this is model manager. for more info look at notion
    # this is for displaying all the rooms that we have created in database i.e. in django backend to display at frontend
    rooms = Room.objects.all() #it overrides the above 'rooms' variable
    # when this function will be triggered, it will render 'home.html' file
    # render function takes 2 parameters: first one 'request' object, second one 'template' that we want to render
    # we have created this 'context' variable just to store the data that we want to pass
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

# anoter route
# our website is going to have rooms for different conversations so we are creating a route for it
def room(request, pk):
    # below code is for dynamically getting values of 'rooms' in respective url with id
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}
    return render(request, 'base/room.html', context)