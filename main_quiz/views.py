from django.shortcuts import render
from .models import TimesTable

def index(request):
    """The home page for mulipleChoice multiplication. Pass request object as parameter to render function, template as other parameter"""
    return render(request, 'main_quiz/index.html')

def practice_mode(request):
    """Show all times tables."""
    times_tables = TimesTable.objects.all()
    context = {'times_tables': times_tables}
    return render(request, 'main_quiz/practice_mode.html', context)

def quiz_mode(request):
    """Determine quiz with lowest percentage, and show this to the user."""
    weakest_times_table = TimesTable.objects.order_by('-average_percentage')[11]
    context = {'weakest_times_table': weakest_times_table}
    return render(request, 'main_quiz/quiz_mode.html', context)

