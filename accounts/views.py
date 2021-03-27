
import django
import os
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from rest_framework import generics, status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from .emotion import func
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
    filterset_fields = ('job_title', 'job_topic', 'category',)
    queryset = JobListings.objects.all()
    # def get_queryset(self, *args, **kwargs):
    #     query_params = self.request.query_params
    #     if "pk" in self.kwargs:
    #         return JobListings.objects.all()
    #     else:
    #         return JobListings.objects.all()[:100]


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

            return Response({'success': 'Created Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmotionAnalysis(APIView):
    def get(self, *args, **kwargs):
        user = self.request.user
        question = self.request.query_params.get('question')

        p = PracticeInterview.objects.filter(
            user=user, question=question).first()
        vid = p.video_upload.url
        print('*******************************************************', vid)
        two_up = os.path.dirname(os.path.dirname(__file__))
        print(two_up)
        pp = two_up + str(vid)
        emotion_dict = func(pp)
        p.emotion = str(emotion_dict)
        p.save()

        return Response(emotion_dict, status=status.HTTP_200_OK)


class CompanyQuestionViewset(viewsets.ModelViewSet):
    model = CompanyQuestion
    serializer_class = CompanyQuestionSerializer
    queryset = CompanyQuestion.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('company', )


class CompanyViewset(viewsets.ModelViewSet):
    model = Company
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('name', )
