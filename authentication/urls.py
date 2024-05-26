'''Defines url patterns for authentication'''
from django.urls import path
from . import views

app_name = "authentication"
urlpatterns = [
    path('student-signup/', views.StudentSignUp.as_view(), name='student_signup'),
    path('teacher-signup/', views.TeacherSignUp.as_view(), name='teacher_signup'),
]