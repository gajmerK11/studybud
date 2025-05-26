from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    # this is core url of the project. what the below code is saying is when user comes to empty string '' route i.e. home page, go ahead and use include() function and this include function sends the user to the urls file of base which is an app of our project
    # we are also letting 'urls.py' file of our app 'base' to take care of all the routing  
    path('', include('base.urls'))
]
