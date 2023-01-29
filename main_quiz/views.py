from django.shortcuts import render
from .models import TimesTable, Question, QuestionOverview
from .import int2string
from django.contrib.auth.decorators import login_required

def index(request):
    """The home page for mulipleChoice multiplication. Pass request object as parameter to render function, template as other parameter"""
    return render(request, 'main_quiz/index.html')

@login_required
def practice_mode(request):
    """Show all times tables."""
    times_tables = TimesTable.objects.all()
    context = {'times_tables': times_tables}
    return render(request, 'main_quiz/practice_mode.html', context)

@login_required
def quiz_mode(request):
    """Determine quiz with lowest percentage, and show this to the user."""
    weakest_times_table = TimesTable.objects.order_by('-average_percentage')[11]
    context = {'weakest_times_table': weakest_times_table}
    return render(request, 'main_quiz/quiz_mode.html', context)

@login_required
def times_table(request, times_table_id):
    """Show a times table and all of the questions within that times table."""
    # Get questions associated with the specific times table
    questions = Question.objects.filter(times_table__pk=times_table_id)
    # Get the question overview associated with the current user completing the quiz.
    user_question_overview = QuestionOverview.objects.filter(owner=request.user)[0]
    # Define attributes as strings that will later be used to modify the average times table percentage for given times table
    string_id = int2string.int_to_string(times_table_id)
    unique_avg = f'{string_id}_avg'
    times_table_name = string_id.title()

    
    if request.method == 'POST':
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
        current_percentage = getattr(user_question_overview, unique_avg)
        percentage = int((score / 12) * 100)
        updated_average = int((current_percentage + percentage) / 2)
        setattr(user_question_overview, unique_avg, updated_average)
        user_question_overview.save()
        context = {'quiz_percentage': percentage}
        return render(request, 'main_quiz/results.html', context)
    else:
        # GET request, build a quiz for user to complete.
        context = {'times_table': times_table_name, 'questions': questions}
        return render(request, 'main_quiz/times_table.html', context)
