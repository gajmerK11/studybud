from django.shortcuts import get_object_or_404, redirect, render
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
# imported from django documentation (after searching 'django flash messages')
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# login view function
def loginPage(request):
    
    page = 'login'

    # restricting logged in user from going back to login page
    if request.user.is_authenticated:
        return redirect('home')

    # here we are getting username and password from login form (request.method == 'POST' means when user submits the form)
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # making sure the user exists
        try:
            user = User.objects.get(username=username)
        except:
            # copied from documentation of django after searching 'django flash messgaes'
            messages.error(request, 'User does not exist')

        # here we are authenticating user. Meaning if user does exist then we are checking his credentials
        user = authenticate(request, username=username, password=password)

        # Then here we are logging in user. 'if user is not None' means if 'user' exists
        if user is not None:
            # this adds 'session' in the database and in the browser
            login(request, user)
            # after user is logged in we are taking him to home page
            return redirect('home')
        
        # here else means 'if user does not exist'
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

# logout view function
def logoutUser(request):

    # this deletes that 'session'
    logout(request)

    return redirect('home')

# register view function
def registerPage(request):
    
    # --- Processing registration form data ---
    # Initializes a blank user registration form.
    form = UserCreationForm()

    # Checks if the user has submitted the registration form.
    if request.method == 'POST':

        # Creates a new form using the user submitted data (request.POST) and that is stored in 'form'
        form = UserCreationForm(request.POST)

        # Checks if the submitted form data is valid
        if form.is_valid():

            # Creates/Registers a new User object from the form stores it in variable 'user' but doesn't save it to the database yet due to 'commit=False'. 'commit=False' lets you modify the user object before saving so that for example if user has typed in their username in full capital then before saving it to database we can modify that username as done below 
            user = form.save(commit=False)
            
            # Converts the username to lowercase before saving to database. This helps prevent duplicate users like John and john.
            user.username = user.username.lower()

            # Saves the new user to the database.
            user.save()

            # Logs the user in automatically after registration.
            login(request, user)
            
            # Redirects the newly registered and logged-in user to the home page.
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    # ------------------------------------------------------- #

    return render(request, 'base/login_register.html', {'form':form})


# view function for 'home.html'
def home(request):

    # This line of code is getting the query parameter 'q' from the URL
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # here we are filtering the rooms as per the topic names or name of the room or description in the room. This is because it enables user to search the rooms either by topic name or room name or by description. Q here is (not a separate library) a class provided by Django that allows us to use AND, OR operations.
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )
    
    # here we are getting all the topics from Topic model so that they can be displayed in home page
    topics = Topic.objects.all()

    room_count = rooms.count()

    # This fetches all the messages/comments that satisfies the filtering condition
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    # when this function will be triggered, it will render 'home.html' file
    # render function takes 2 parameters: first one 'request' object, second one 'template' that we want to render
    # we have created this 'context' variable just to store the data that we want to pass
    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count, 'room_messages': room_messages}

    return render(request, 'base/home.html', context)



# room view function 
def room(request, pk):

    # below code is for dynamically getting values of 'rooms' in respective url with id
    room = None

    # below code is model manager. get() method returns one single item. Since get returns one single item, we need to get this by a unique value because let's say we have two items with the same value like a 'name' or sth like that it's gonna throw an error because it needs to get back single object. That's why in this case we are gonna specify the value that we wanna get it by as 'id=pk'
    room = Room.objects.get(id=pk)

    # This line of code is saying give us all set of messages related to this specific room. 
    # In django, we can query the child of a parent model (here Message is the child of parent model Room) like this i.e. by using small letter of model name not Message but message
    # '.order_by('-created')' displays recent messages at top
    room_messages = room.message_set.all()

    # Fetching all the participants for displaying them
    # "room.participants.all()" in this we are able to use 'room.participants' due to related_name=participants. If we have not used 'related_name=participants' then we have to use 'user.room_set.all()'
    participants = room.participants.all()

    # Logic to create message i.e. comment
    # When user submits the message via "Write your message here" form 
    if request.method == 'POST':

        # Creates the message. Here we are using 'Message' model because that's the model we have created for messages.
        # The below code is saying create a message with the current user, current room and the types message body.
        message = Message.objects.create(

            # It links the message to the currently logged-in user who is sending the message.
            user = request.user,

            # It associates the message with the current room i.e. it keeps the message in the current room
            room = room,

            # It fetches the actual message content that the user typed in the message form in 'room.html'
            body = request.POST.get('body')
        )

        # It adds new user as Participants if he writes a message / comment 
        room.participants.add(request.user)

        # After the message is created, this line redirects the user back to the same room page that's why "pk=room.id" is used to know the exact location of current room. 
        return redirect('room', pk=room.id)

    context = {'room': room,'room_messages':room_messages,'participants':participants}
    return render(request, 'base/room.html', context)

# userprofile view function
# This handles the display of a user’s profile page. pk (primary key) is passed in the URL to identify which user’s profile to show.
def userProfile(request, pk):

    # This line fetches the user object from Django's built-in User model using the given id.
    user = User.objects.get(id=pk)
    
    # This gets all the rooms created by that user. It uses Django’s reverse relationship through ForeignKey(host, ...) in the Room model.
    rooms = user.room_set.all()

    # This gets all the messages/comments that the user has posted.
    room_messages = user.message_set.all()

    # This gets all available topics so that you can show them on the user profile page
    topics = Topic.objects.all()

    context = {'user':user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics }
    
    return render(request, 'base/profile.html', context)



# This function is responsible for DISPLAYING a form to the user and SAVING the form data to the database when the user submits it.
@login_required(login_url='login')
def createRoom(request):

    # This creates a blank form from the RoomForm class. It’s shown to the user when they first open the page.
    form = RoomForm()

    # This checks if the user has submitted the form (a POST request means form submission).
    if request.method == 'POST':
        
        # This fills the form with the data the user submitted.
        form = RoomForm(request.POST)

        # This checks if the submitted form data is valid (e.g., all required fields are filled out properly).
        if form.is_valid():

            # Here what we are doing is, we want the user one who is logged in to be the host of the every room he creates. 
            # So the below line of code says "Create a room instance from the form without saving it to the database yet due to 'commit=False'."
            room = form.save(commit=False)

            # Here we are making one who is logged in i.e. 'request.user' as the host of the room 'room.host'.
            room.host = request.user

            # Saves the room instance to database
            room.save()

            # After saving, the user is redirected to the home page (usually a list of rooms or dashboard).
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# This function is for updating an existing room
# 'pk' parameter helps us to know which room we are updating i.e. 'pk' here is the unique ID of the room we want to update
@login_required(login_url='login')
def updateRoom(request, pk):

    # gets the room using given id
    room = Room.objects.get(id=pk)

    # here we are getting the form and 'instance=room' provides us form with pre-filled data of Room that we get from above line of code
    form = RoomForm(instance=room)

    # here we are restricting a user to edit other user's created rooms (i.e. room not created by him; he is not the host)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

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

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    # here we are restricting a user to delete other user's created rooms (i.e. room not created by him; he is not the host)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

# view function for deleting comment
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = get_object_or_404(Message, id=pk)
    # room = message.room
    
    
    # if request.user != message.user:
    #     return HttpResponse('You are not allowed here!!')
    
    # This processes the data from delete.html
    if request.method == 'POST':
        message.delete()
        # return redirect('room', pk=room.id)
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})