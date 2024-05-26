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

class TeacherProfile(models.Model):
    """Model used to represent profile for teacher"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="teacher_profile")
    teacher_name = models.CharField(max_length=200)

    def __str__(self):
        return self.teacher_name.title()
    
class StudentProfile(models.Model):
    """Model used to represent profile for student"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey('main_quiz.Classroom', on_delete=models.SET_NULL, null=True, blank=False)
    
