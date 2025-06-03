from django.db import models

# we are inheriting from 'models' and this is what's gonna change it from standard python class to actual django model or basically database table
class Room(models.Model):
    #host = 
    #topic = 
    name = models.CharField(max_length=200)
    # here 'null=True' means that this can be blank i.e. 'description' column can be empty
    # here 'blank=True' means when we run the save method like when we submit the form, that form can also be empty
    # 'null=True' is for database and 'blank=True' is for save method like when we are adding the form
    # these two are for the scenario "maybe someone created a room and they didn't add the description they wanna add it later, we wanna let them do that and we will just allow them to update that later"
    description = models.TextField(null=True, blank=True)
    #participants =
    # this 'updated' gonna take the snapshot of any time this model instance was updated so anytime we run the save method to update this model i.e. this specific table, its gonna take the timestamp
    # here 'auto_now=True' means every time the save method is called go ahead and take the timestamp
    updated = models.DateTimeField(auto_now=True)
    # updated and created are similar but the difference between auto_now and auto_now_add is that auto_now takes the timestamp every time we save the item but auto_now_add only takes the timestamp when we FIRST save or create this instance
    # so if we save it multiple times 'created' value will never change because of auto_now_add but 'updated' value will change everytime because of auto_now
    # basically this 'updated' and 'created' is for knowing when was any room created and when was the last time it was updated  
    created = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name

