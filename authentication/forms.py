from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from django import forms as d_forms
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

class CustomSignupForm(SignupForm):
    first_name = d_forms.CharField(required=True, widget=d_forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = d_forms.CharField(required=True, widget=d_forms.TextInput(attrs={'placeholder': 'Last name'}))