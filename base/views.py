from django.shortcuts import redirect, render
from .models import Room, Topic
from .forms import RoomForm



# view function for 'home.html'
def home(request):
    # This line of code is getting the query parameter 'q' from the URL
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # here we are filtering the rooms as per the topic names given by the user i.e. give me those rooms which have topic matching what the user typed or clicked (value of q)
    rooms = Room.objects.filter(topic__name__icontains=q)
    # here we are getting all the topics from Topic model so that they can be displayed in home page
    topics = Topic.objects.all()
    # when this function will be triggered, it will render 'home.html' file
    # render function takes 2 parameters: first one 'request' object, second one 'template' that we want to render
    # we have created this 'context' variable just to store the data that we want to pass
    context = {'rooms': rooms, 'topics':topics}
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


# This function is responsible for DISPLAYING a form to the user and SAVING the form data to the database when the user submits it.
def createRoom(request):
    # This creates a blank form from the RoomForm class. It’s shown to the user when they first open the page.
    form = RoomForm()

    # This checks if the user has submitted the form (a POST request means form submission).
    if request.method == 'POST':
        # This fills the form with the data the user submitted.
        form = RoomForm(request.POST)
        # This checks if the submitted form data is valid (e.g., all required fields are filled out properly).
        if form.is_valid():
            # If the form is valid, this saves the data into the database, creating a new Room object
            form.save()
            # After saving, the user is redirected to the home page (usually a list of rooms or dashboard).
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# This function is for updating an existing room
# 'pk' parameter helps us to know which room we are updating i.e. 'pk' here is the unique ID of the room we want to update
def updateRoom(request, pk):
    # gets the room using given id
    room = Room.objects.get(id=pk)
    # here we are getting the form and 'instance=room' provides us form with pre-filled data of Room that we get from above line of code
    form = RoomForm(instance=room)

    # These below lines of code are for editing / updating
    # This checks if the user has submitted the form (here submiting the form means providing edited/updated form)
    if request.method == 'POST':
        # This line grabs the submitted data from the form and uses it to update the room instance.
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})