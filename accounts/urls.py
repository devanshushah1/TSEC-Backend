from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'joblisting', views.JobListingViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/employee', views.SignupEmployee.as_view(), name='signup'),
    path('signup/company', views.SignupCompany.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
]