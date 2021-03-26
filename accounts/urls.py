from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/employee', views.SignupEmployee.as_view(), name='signup'),
    path('signup/company', views.SignupCompany.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
]