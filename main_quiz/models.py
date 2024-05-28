from django.db import models
import uuid
from authentication.models import TeacherProfile

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