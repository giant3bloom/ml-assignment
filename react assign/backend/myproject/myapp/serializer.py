from rest_framework import serializers
from .models import UserInput

class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInput
        fields = ['year', 'km_driven', 'seler_type', 'fuel_type', 'transmission_type', 'owner']
