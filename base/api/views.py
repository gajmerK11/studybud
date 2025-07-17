from rest_framework.decorators import api_view
from rest_framework.response import Response


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