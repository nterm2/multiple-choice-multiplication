"""Defines URL patterns for main_quiz"""

from django.urls import path
from . import views

#Distiguish this URL from other URL's from other Django apps
app_name = 'main_quiz'
urlpatterns = [
    #Defining the URL pattern used to access the homepage, once this URL has been entered, the fucntion index() from the file views will be called. Name attribute allows us to refrence this URL in other sections of code.
    path('', views.index, name='index'),
    path('practice-mode/', views.practice_mode, name='practice_mode'),
    # Detail page for a single times table.
    path('start-quiz/<int:times_table_id>/', views.times_table, name='start_quiz'),
    path('my-question-overview/', views.question_overview, name='question_overview'),
    path('leaderboard/<int:times_table_id>/', views.leaderboard, name='leaderboard'),
    path('all-leaderboards/', views.all_leaderboards, name='all_leaderboards'),
    path('teacher-overview/', views.teacher_overview, name='teacher_overview'),
    path('create-classroom/', views.create_classroom, name='create_classroom'),
    path('update-classroom/<int:id>/', views.update_classroom, name='update_classroom'),
    path('delete-classroom/<int:id>/', views.delete_classroom, name='delete_classroom'),
    path('classroom-overview/<int:id>/', views.classroom_overview, name='classroom_overview'),
    path('student-overview/', views.student_overview, name='student_overview'),
    path('quiz-mode-preview/', views.quiz_mode_preview, name='quiz_mode_preview'),
    path('practice-mode-preview/', views.practice_mode_preview, name='practice_mode_preview'),
]