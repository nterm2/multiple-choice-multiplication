from django.db import models
import uuid
from authentication.models import TeacherProfile
from django.contrib.auth import get_user_model

class TimesTable(models.Model):
    """Represents the values associated for a given times table."""
    times_table = models.IntegerField()

    def __str__(self):
        """Return a string representation of the TimesTable model"""
        return f'Times Table: {self.times_table}'

class Question(models.Model):
    """Model representing a question"""
    times_table = models.ForeignKey(TimesTable, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    answer = models.IntegerField()

class Classroom(models.Model):
    """Model representing a classroom"""
    classroom_code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    classroom_name = models.CharField(max_length=100)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    def __str__(self):
        return self.classroom_name

class Submission(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="quiz_submissions")
    timetable = models.ForeignKey(TimesTable, on_delete=models.CASCADE, related_name="quiz_submissions")
    date_taken = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} got {self.score}% for the {self.timetable} times table at {self.date_taken}'