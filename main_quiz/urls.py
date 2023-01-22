"""Defines URL patterns for main_quiz"""

from django.urls import path
from . import views

#Distiguish this URL from other URL's from other Django apps
app_name = 'main_quiz'
urlpatterns = [
    #Defining the URL pattern used to access the homepage, once this URL has been entered, the fucntion index() from the file views will be called. Name attribute allows us to refrence this URL in other sections of code.
    path('', views.index, name='index'),
]