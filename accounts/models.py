from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_employer(self, email, password, **extra_fields):
        user = self.create_user(email, password)
        user.is_employer = True
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    is_employer = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class job_listing(models.Model):
    job_topic = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    job_requirements = models.TextField(blank=True, null=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    job_location = models.TextField(blank=True, null=True)
    job_salary = models.CharField(max_length=255, blank=True, null=True)
    job_qualification = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.CharField(max_length=255, null=True, blank=True)
    job_experience = models.CharField(max_length=255, null=True, blank=True)
    job_link = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.job_title