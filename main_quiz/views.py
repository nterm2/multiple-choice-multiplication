from django.shortcuts import render, redirect
from .models import TimesTable, Question, Classroom
from . import int2string
from django.contrib.auth.decorators import login_required
import json
from .forms import ClassroomForm
from authentication.models import StudentProfile
#Import Graphing Libraries
import plotly.express as px

def index(request):
    """The home page for mulipleChoice multiplication. Pass request object as parameter to render function, template as other parameter"""
    return render(request, 'index.html')

@login_required
def all_leaderboards(request):
    times_tables = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    context = {'times_tables': times_tables}
    return render(request, 'all_leaderboards.html', context)

@login_required
def leaderboard(request, times_table_id):
    """View that will provide the data for a leaderboard specific to a times table"""
    all_overviews = QuestionOverview.objects.all()
    students = []
    class_percentages = []
    times_table_name = f"{int2string.int_to_string(times_table_id)}_avg"
    for overview in all_overviews:
        owner_object = overview.owner 
        students.append(owner_object.username)
        # Get average percentage for relevant times table.
        class_percentages.append(getattr(overview, times_table_name))
    # plot_div = plot([Bar(x=students, y=class_percentages)], output_type='div')
    fig = px.bar(
        x=students,
        y=class_percentages,
        title=f"{int2string.int_to_string(times_table_id).title()} Times Table Leaderboard",
        labels={'x': 'Students', 'y': f"Average {int2string.int_to_string(times_table_id)} times table scores (%)"}
    )
    fig.update_layout(yaxis_range=[0,100])
    chart = fig.to_html()
    context = {'chart': chart}
    return render(request, 'leaderboard.html', context)


@login_required
def practice_mode(request):
    """Show all times tables."""
    times_tables = TimesTable.objects.all()
    context = {'times_tables': times_tables}
    return render(request, 'practice_mode.html', context)

@login_required
def teacher_overview(request):
    teacher_profile = request.user.teacher_profile
    classrooms = Classroom.objects.filter(teacher=teacher_profile)
    print(classrooms)
    context = {'classrooms': classrooms, 'teacher_profile': teacher_profile}
    return render(request, 'teacher_overview.html', context)

@login_required
def create_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = request.user.teacher_profile
            classroom.save()
        return redirect("main_quiz:teacher_overview")
    else:
        form = ClassroomForm()
    
    context = {'form': form}
    return render(request, "create_classroom.html", context=context)

@login_required
def update_classroom(request, id):
    instance = Classroom.objects.get(id=id)
    form = ClassroomForm(request.POST or None, instance=instance)
    if form.is_valid():
        classroom = form.save()
        return redirect("main_quiz:teacher_overview")        
    context = {'form': form, 'classroom': instance}
    return render(request, 'update_classroom.html', context=context)

@login_required
def delete_classroom(request, id):
    instance = Classroom.objects.get(id=id)
    if request.method == 'POST':
        instance.delete()
        return redirect("main_quiz:teacher_overview") 
    context = {'classroom': instance}       
    return render(request, 'delete_classroom.html', context=context)

@login_required
def classroom_overview(request, id):
    classroom = Classroom.objects.get(id=id)
    students = StudentProfile.objects.filter(classroom=classroom)
    context = {'classroom': classroom, 'students': students}
    return render(request, 'classroom_overview.html', context=context)

@login_required 
def student_overview(request):
    user = request.user
    context = {"user": user}
    return render(request, 'student_overview.html', context=context)

@login_required
def quiz_mode_preview(request):
    times_tables = TimesTable.objects.all()
    user = request.user
    context = {"times_tables": times_tables, "user": user}
    return render(request, 'quiz_mode_preview.html', context=context)

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
    return render(request, 'quiz_mode.html', context)

@login_required
def question_overview(request):
    """Show question overview for a single student"""
    overview = QuestionOverview.objects.filter(owner=request.user)[0]
    context = {'overview': overview}
    return render(request, 'question_overview.html', context)

@login_required
def times_table(request, times_table_id):
    """Show a times table and all of the questions within that times table."""
    # Get questions associated with the specific times table
    questions_all = Question.objects.all()
    questions = []
    for question in questions_all:
        if question.times_table.times_table == times_table_id:
            questions.append(question)
        else:
            pass
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
        context = {'quiz_percentage': percentage}
        return render(request, 'results.html', context)
    else:
        # GET request, build a quiz for user to complete.
        context = {'times_table': times_table_name, 'questions': questions}
        return render(request, 'times_table.html', context)
