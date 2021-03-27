from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'joblisting', views.JobListingViewset, basename="JobListing")
router.register(r'interview-questions', views.InterviewQuestionsViewset)
router.register(r'practice-interview', views.PracticeInterviewViewset)
router.register(r'company-question', views.CompanyQuestionViewset)
router.register(r'company', views.CompanyViewset)



urlpatterns = [
    path('', include(router.urls)),
    path('signup/employee', views.SignupEmployee.as_view(), name='signup'),
    path('signup/company', views.SignupCompany.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('emotion/', views.EmotionAnalysis.as_view(), name='emotion'),
]
