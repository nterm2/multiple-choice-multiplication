from django.shortcuts import render
from .models import TimesTable, Question, QuestionOverview
from . import int2string
from django.contrib.auth.decorators import login_required
import json

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
    user_question_overview = QuestionOverview.objects.filter(owner=request.user)[0]
    percentages = []
    for i in range(1, 13):
        current_times_table = int2string.int_to_string(i)
        current_avg = f"{current_times_table}_avg"
        current_percentage = getattr(user_question_overview, current_avg)
        percentages.append(current_percentage)
    weakest_times_table = percentages.index(min(percentages)) + 1

    context = {'weakest_times_table': weakest_times_table}
    return render(request, 'main_quiz/quiz_mode.html', context)

@login_required
def question_overview(request):
    """Show question overview for a single student"""
    overview = QuestionOverview.objects.filter(owner=request.user)[0]
    context = {'overview': overview}
    return render(request, 'main_quiz/question_overview.html', context)

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
    unique_avg_list = f'{string_id}_average_list'
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
        # Deals with retrieving and storing averages
        averages_list = json.loads(getattr(user_question_overview, unique_avg_list))
        # Ensure that all elements in list are stored as integers to prevent errors
        averages_list = [int(average) for average in averages_list]
        #Calculate percentage from quiz, store in list, and set new average for corresponding times table.
        percentage = int((score / 12) * 100)
        averages_list.append(percentage)
        new_average = int(sum(averages_list) / len(averages_list))
        setattr(user_question_overview, unique_avg, new_average)
        # Save new list of percentages to database.
        averages_json_format = json.dumps(averages_list)
        setattr(user_question_overview, unique_avg_list, averages_json_format)
        user_question_overview.save()

        user_question_overview.save()
        context = {'quiz_percentage': percentage}
        return render(request, 'main_quiz/results.html', context)
    else:
        # GET request, build a quiz for user to complete.
        context = {'times_table': times_table_name, 'questions': questions}
        return render(request, 'main_quiz/times_table.html', context)
