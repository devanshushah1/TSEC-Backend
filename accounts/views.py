
import django
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from rest_framework import generics, status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import django_filters.rest_framework


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.

class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SignupEmployee(APIView):
    def post(self, request):
        password = request.data.get('password')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        first_name = request.data.get('first_name')

        user = CustomUser.objects.create_user(email, password)
        user.phone_number = phone_number
        user.first_name = first_name
        user.save()
        data = {}
        data['email'] = email
        data['phone_number'] = phone_number
        return Response(data, status=status.HTTP_201_CREATED)


class SignupCompany(APIView):
    def post(self, request):
        password = request.data.get('password')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        company_name = request.data.get('company_name')

        user = CustomUser.objects.create_employer(email, password)
        user.phone_number = phone_number
        user.company_name = company_name
        user.save()
        data = {}
        data['email'] = email
        data['phone_number'] = phone_number
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token = get_tokens_for_user(user)
        user_data = {
            'token': token,
            'user': {
                'userid': user.id,
                'emailid': user.email,
                'is_employer': user.is_employer
            }
        }
        return Response(user_data, status=status.HTTP_200_OK)

# class CustomUserView()


class JobListingViewset(viewsets.ModelViewSet):
    model = JobListings
    serializer_class = JobListingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('job_title', 'job_topic',)

    def get_queryset(self, *args, **kwargs):
        query_params = self.request.query_params
        if "pk" in self.kwargs:
            return JobListings.objects.all()
        else:
            return JobListings.objects.all()[:100]


class InterviewQuestionsViewset(viewsets.ModelViewSet):
    model = InterviewQuestions
    serializer_class = InterviewQuestionsSerializer
    queryset = InterviewQuestions.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('category', )


class PracticeInterviewViewset(viewsets.ModelViewSet):
    model = PracticeInterview
    serializer_class = PracticeInterviewSerializer
    queryset = PracticeInterview.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('question', 'user', 'share_it',)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            prac = serializer.save()
            prac.user = request.user
            prac.save()
            # x = model_to_dict(prac)
            
            return Response({'success':'Created Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# ---------------------------------------------------------------------------------------------------------------

import numpy as np      
import argparse
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
from tensorflow.keras.models import load_model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
ap = argparse.ArgumentParser()
ap.add_argument("--mode",help="train/display")
mode = ap.parse_args().mode

model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))
model.load_weights('emotion.h5')

cv2.ocl.setUseOpenCL(False)

emotion = {0: "Angry", 1: "Disgusted", 2: "Fearful", 
           3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

def FrameCapture(path):
    counter = {
        "Angry":0,
        "Disgusted":0,
        "Fearful":0,
        "Happy":0,
        "Neutral":0,
        "Sad":0,
        "Surprised":0
    }
    # Path to video file
    vidObj = cv2.VideoCapture(path)
  
    # Used as counter variable
    count = 0
  
    # checks whether frames were extracted
    success = 1
  
    while success:
        # vidObj object calls read
        # function extract frames
        success, frame = vidObj.read()
        # Saves the frames with frame-count
        if not success:
            break
        face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        finalface = face.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)
        print('abc', finalface)
        print(456)

        for (x, y, w, h) in finalface:
            finalgray = gray[y:y + h, x:x + w]
            cropimg = np.expand_dims(np.expand_dims(cv2.resize(finalgray, (48, 48)), -1), 0)
            predict = model.predict(cropimg)
            maxi = int(np.argmax(predict))
            counter[emotion[maxi]]+=1
            print(123)
    
    return counter

print(FrameCapture('WIN_20210327_15_45_31_Pro.mp4'))

