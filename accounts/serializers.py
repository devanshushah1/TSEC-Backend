from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('__all__')

class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = job_listing
        fields = ('__all__')

        