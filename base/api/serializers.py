# Our serializers are going to be classes that takes a certain model (database classes) that we want to serialize and turn it into json data. Basically, it is for converting python objects into json.

from rest_framework.serializers import ModelSerializer
from base.models import Room

# What this class does is, it takes Room model (defined in models.py) and turns its all fields (i.e. fields = '__all__) into json
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'