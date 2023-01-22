"""Define URL patterns for users"""

from django.urls import path, include

from . import views 

# DIstinguish this URL file from other urls.py files from other apps in this project by setting app_name to 'users'
app_name = 'users'
urlpatterns = [
    # Include default auth urls to authenticate users rather than doing it myserlf.
    path('', include('django.contrib.auth.urls')),
    # Registration page
    path('register/', views.register, name='register')
]