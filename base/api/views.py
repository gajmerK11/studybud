from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer


# view function to handle incoming requests
@api_view(['GET']) # Restrict this view to only handle GET requests
def getRoutes(request):
    # List of available API routes
    routes = [
        # Route to get all the api endpoints information 
        'GET /api',
        # Route to get all rooms
        'GET /api/rooms',
        # Route to get a specific room by ID
        'GET /api/rooms/:id'
    ] 
    # Return the routes as a JSON response using DRF's Response class
    return Response(routes)

# view function to display all the rooms
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

# view function to display single room
@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)