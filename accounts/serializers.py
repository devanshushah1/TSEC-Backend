from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('__all__')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


class JobListingSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = JobListings
        fields = ('__all__')


class InterviewQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestions
        fields = ('__all__')


class PracticeInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeInterview
        fields = ('__all__')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('__all__')


class CompanyQuestionSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = CompanyQuestion
        fields = ('__all__')
