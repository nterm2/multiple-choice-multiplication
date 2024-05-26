from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from django import forms as d_forms
from .models import User, TeacherProfile, StudentProfile
from main_quiz.models import Classroom

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = {
            "first_name",
            "last_name",
            "email",
            "is_student",
            "is_teacher"
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = {
            "first_name",
            "last_name",
            "email",
            "is_student",
            "is_teacher"
        }

class TeacherSignupForm(SignupForm):
    first_name = d_forms.CharField(required=True, widget=d_forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = d_forms.CharField(required=True, widget=d_forms.TextInput(attrs={'placeholder': 'Last name'}))
    teacher_name = d_forms.CharField(required=True, widget=d_forms.TextInput(attrs={'placeholder': 'Teacher name'}))

    def save(self, request):
        user = super(TeacherSignupForm, self).save(request)
        teacher_profile = TeacherProfile(user=user, teacher_name=self.cleaned_data.get('teacher_name'))
        teacher_profile.save()
        return teacher_profile.user


def validate_classroom_code(classroom_code):
    try:
        classroom = Classroom.objects.get(classroom_code=classroom_code)
    except Classroom.DoesNotExist:
        raise d_forms.ValidationError("Invalid classroom code")
    
class StudentSignupForm(SignupForm):
    first_name = d_forms.CharField(required=True, widget=d_forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = d_forms.CharField(required=True, widget=d_forms.TextInput(attrs={'placeholder': 'Last name'}))
    classroom_code = d_forms.CharField(required=True, widget=d_forms.TextInput(attrs={'placeholder': 'Classroom code'}), validators=[validate_classroom_code])

    def save(self, request):
        user = super(StudentSignupForm, self).save(request)
        classroom_to_join = Classroom.objects.get(classroom_code=self.cleaned_data.get('classroom_code'))
        student_profile = StudentProfile(user=user, classroom=classroom_to_join)
        student_profile.save()
        return student_profile.user
