from django.shortcuts import render
from .models import TimesTable, Question

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

def times_table(request, times_table_id):
    """Show a times table and all of the questions within that times table."""
    # Get individual times table object
    times_table = TimesTable.objects.get(id=times_table_id)
    # Get questions associated with the specific times table
    questions = Question.objects.filter(times_table__pk=times_table_id)
    context = {'times_table': times_table, 'questions': questions}

    # Retrieve list answers from users form when they submit it
    user_answers = dict(request.POST)
    del user_answers['csrfmiddlewaretoken']
    user_answers = user_answers.values()
    user_answers = sum(user_answers, [])

    # Now they can be compared against the answers for the questions, and a percentage can be calculated.
    score = 0
    for i in range(12):
        user_answer = user_answers[i]
        actual_answer = questions[i].answer
        if int(user_answer) == actual_answer:
            score += 1
    percentage = int((score / 12) * 100)
    print(percentage)


    return render(request, 'main_quiz/times_table.html', context)
