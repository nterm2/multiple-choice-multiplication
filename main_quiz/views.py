from django.shortcuts import render, redirect
from .models import TimesTable, Question, Classroom, Submission
from . import int2string
from django.contrib.auth.decorators import login_required
from .forms import ClassroomForm
from authentication.models import StudentProfile
import random
#Import Graphing Libraries
import plotly.express as px
import ast

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
    user = request.user
    submissions = user.quiz_submissions.all()
    if len(submissions) == 0 or len(submissions) == 1:
        weakest_timestable = None 
    else:
        user_averages = {}
        all_times_tables = TimesTable.objects.all()
        for times_table in all_times_tables:
            users_time_table_submissions = submissions.filter(timetable=times_table)
            if len(users_time_table_submissions) != 0:
                sum_of_scores = 0
                for submission in users_time_table_submissions:
                    sum_of_scores += submission.score
                average = int(sum_of_scores / len(users_time_table_submissions))
                user_averages[times_table] = average
        user_averages = dict(sorted(user_averages.items(), key=lambda item: item[1]))
        weakest_timestable = list(user_averages.keys())[0]
                

    context = {"user": user, 'weakest_times_table': weakest_timestable}
    return render(request, 'quiz_mode_preview.html', context=context)

@login_required
def practice_mode_preview(request):
    times_tables = TimesTable.objects.all()
    context = {'times_tables': times_tables}
    return render(request, 'practice_mode_preview.html', context=context)

@login_required
def question_overview(request):
    """Show question overview for a single student"""
    user = request.user
    submissions = user.quiz_submissions.all()
    user_averages = {}
    all_times_tables = TimesTable.objects.all()
    for times_table in all_times_tables:
        users_time_table_submissions = submissions.filter(timetable=times_table)
        if len(users_time_table_submissions) != 0:
            sum_of_scores = 0
            for submission in users_time_table_submissions:
                sum_of_scores += submission.score
            average = int(sum_of_scores / len(users_time_table_submissions))
            user_averages[times_table] = average
        else: 
            user_averages[times_table] = None 
    context = {'overview': user_averages, 'user': request.user}
    return render(request, 'question_overview.html', context)


def generate_options(answer):
    """Returns list containing answer and three random, non-duplicate integers between range of 1-12 times tables (1-144)"""
    options = []
    count = 0
    while count < 3:
        random_number = random.randint(1, 144)
        if (random_number != answer ) and (random_number not in options):
            options.append(random_number)
            count += 1
        else:
            pass
    options.append(answer)
    random.shuffle(options)
    return options

@login_required
def times_table(request, times_table_id):
    times_table = TimesTable.objects.get(id=times_table_id)
    if request.method == 'GET':
        questions = Question.objects.filter(times_table=times_table)
        questions_custom_array = []
        for question in questions:
            question_dict = {}
            question_dict["question_text"] = question.question_text
            question_dict["answer"] = question.answer 
            question_dict["options"] = generate_options(question.answer)
            questions_custom_array.append(question_dict)
        random.shuffle(questions_custom_array)
        context = {"times_table": times_table.times_table, "questions": questions_custom_array}
        return render(request, 'start_quiz.html', context) 
    
    elif request.method == 'POST':
        questions = Question.objects.filter(times_table=times_table)
        quiz_data = dict(request.POST)
        del quiz_data['csrfmiddlewaretoken']
        num_correct_answers = 0
        for question_data, answer in quiz_data.items():
            question_data = ast.literal_eval(question_data)
            answer = answer[0]
            if int(question_data['answer']) == int(answer):
                num_correct_answers += 1
        percentage = int((num_correct_answers / len(questions)) * 100)
        new_submission = Submission.objects.create(user=request.user, timetable=times_table, score=percentage)
        context = {"score": new_submission.score}
        return render(request, 'results.html', context=context)
