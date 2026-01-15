from django.db import models
from django.contrib.auth.models import AbstractUser 

# Custom user model (django has default user model which doesn't allow us fields like bio, profile picture so we need to create a custom one)
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# another model 'Topic'. A room is going to be the child of a topic so we are making it above 'Room'
class Topic(models.Model):
    # we have only created one attribute here because 'Topic' is only going to have the name of the topic
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



# we are inheriting from 'models' and this is what's gonna change it from standard python class to actual django model or basically database table
class Room(models.Model):
    # relationship between User and host i.e. somebody has to host the room
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # setting up of relationship between Room and Topic i.e. a Topic can have multiple Rooms whereas a Room can only have one Topic. 'on_delete=models.SET_NULL' means when a Topic is deleted, don't delete the Room instead, just set the Topic of the related Room to NULL (i.e. empty/no topic) and 'null=True' means that 'topic' field in the database can be NULL. If 'null=True' is not set then django will not allow a NULL value in this field and will throw an error.
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    # here 'null=True' means that this can be blank i.e. 'description' column can be empty
    # here 'blank=True' means when we run the save method like when we submit the form, that form can also be empty
    # 'null=True' is for database and 'blank=True' is for save method like when we are adding the form
    # these two are for the scenario "maybe someone created a room and they didn't add the description they wanna add it later, we wanna let them do that and we will just allow them to update that later"
    description = models.TextField(null=True, blank=True)

    # Here we are specifying many-to-many relationship between Room and User. It enables -> One Room can have many Users as participants. -> One User can be in many Rooms. 
    participants = models.ManyToManyField(User, related_name='participants', blank=True)

    # this 'updated' gonna take the snapshot of any time this model instance was updated so anytime we run the save method to update this model i.e. this specific table, its gonna take the timestamp
    # here 'auto_now=True' means every time the save method is called go ahead and take the timestamp
    updated = models.DateTimeField(auto_now=True)
    # updated and created are similar but the difference between auto_now and auto_now_add is that auto_now takes the timestamp every time we save the item but auto_now_add only takes the timestamp when we FIRST save or create this instance
    # so if we save it multiple times 'created' value will never change because of auto_now_add but 'updated' value will change everytime because of auto_now
    # basically this 'updated' and 'created' is for knowing when was any room created and when was the last time it was updated
    # 'updated' and 'created' are timstamp fields for Room model
    created = models.DateTimeField(auto_now_add=True)  

    # This is done so that newly created rooms appear in top. Here 'Meta' class is used because 'Meta' class is used specifically to define metadata(extra information) for a model.Meaning "information about how the model behaves, not what data it holds." And yes even tuple can be used but list is mostly used due to convention.
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

# another model. Each room is gonna have a message
class Message(models.Model):
    # below are the values of Message i.e the things message going to have
    # setting up 'user' relationship that is one-to-many relationship i.e. one user can have many messages but all the messages will be linked up to one user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # look at notion for this code explanation
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # 'body' here is the actual message
    body = models.TextField()
    # 'updated' stores the timestamp of the last time the message was modified
    # 'created' stores the timestamp of when the message was first created (sent)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 

# This method defines how a message object is represented as a string
# It returns the first 50 characters of the message body for a readable summary (Remember it's not in the front end, but rather behind the scenes, in a way we can say in Django admin panel)
    def __str__(self):
        return self.body[0:50]
   
    # It orders recent message at top in Recent Activity
    class Meta:
        ordering = ['-updated', '-created']

