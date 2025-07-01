from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):

    # This 'Meta' class is mandatory in every ModelForm. Without it our model form won't work. Without this, Django has no idea how to generate the form fields or how to connect the form to the database.
    class Meta:

        # This tells Django: “This form is for the Room model.” Django will look at the Room model and automatically generate form fields for it.
        model = Room

        # This means: “Include all fields from the Room model in the form.”
        fields = '__all__'

        # Here, 'exclude' is not a normal variable, it is actually django's ModelForm "a special configuration option".
        # It says django "Don't include these fields in the form"
        exclude = ['host', 'participants']