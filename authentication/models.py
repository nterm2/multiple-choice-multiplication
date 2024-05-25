from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Model containing common fields that will be used for both students and teachers"""
    username = None 
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(_("email address"), unique=True)

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "is_teacher", "is_student"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email