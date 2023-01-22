# Import the render and redirect functions
from django.shortcuts import render, redirect 

# Import login form to log the user in
from django.contrib.auth import login 

#Import class representing a sign up form
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Register a new user"""
    if request.method != 'POST':
        # Display blank registration form.
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)

        # Check if form is valid before saving new user's data.
        if form.is_valid():
            new_user = form.save()
            # Log them in and redirect to home page.
            login(request, new_user)
            return redirect('main_quiz:index')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)

