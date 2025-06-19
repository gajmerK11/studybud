from django.shortcuts import redirect, render
from .models import Room
from .forms import RoomForm

# Create your views here.
# we have created this 'rooms' list of dictionaries to pass data
# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


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
    # below code is model manager. get() method returns one single item. Since get returns one single item, we need to get this by a unique value because let's say we have two items with the same value like a 'name' or sth like that it's gonna throw an error because it needs to get back single object. That's why in this case we are gonna specify the value that we wanna get it by as 'id=pk'
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)


# this function is for rendering the form 'room_form.html' that is used for creating and updating the room without having to go to django admin panel i.e. creating room from frontend. 
# In overall, we can say this function handles the web request for creating a new room.
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)