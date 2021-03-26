from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework import generics, status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class Signup(APIView):
    def post(self, request):
        password = request.data.get('password')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')

        user = CustomUser.objects.create_user(email, password)
        user.phone_number = phone_number
        user.save()
        data = {}
        data['email'] = email
        data['phone_number'] = phone_number
        return Response(data, status=status.HTTP_201_CREATED)
        