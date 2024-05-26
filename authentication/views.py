from django.shortcuts import render
from allauth.account.views import SignupView 

from .forms import TeacherSignupForm
from .forms import StudentSignupForm

class TeacherSignUp(SignupView):
    template_name = "account/teacher-signup.html"
    form_class = TeacherSignupForm
    redirect_field_name = "teacher_overview"
    view_name = "teacher_signup"

class StudentSignUp(SignupView):
    template_name = "account/student-signup.html"
    form_class = StudentSignupForm
    redirect_field_name = "index"
    view_name = "student_signup"
