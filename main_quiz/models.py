from django.db import models
from django.contrib.auth.models import User 

class TimesTable(models.Model):
    """Represents the values associated for a given times table."""
    times_table = models.IntegerField()

    def __str__(self):
        """Return a string representation of the TimesTable model"""
        return f'Times Table: {self.times_table}'

class QuestionOverview(models.Model):
    """Model reprsenting question overview for a student"""
    one_times_table = models.IntegerField(default=1)
    one_avg = models.IntegerField(default=0)

    two_times_table = models.IntegerField(default=2)
    two_avg = models.IntegerField(default=0)

    three_times_table = models.IntegerField(default=3)
    three_avg = models.IntegerField(default=0)
    
    four_times_table = models.IntegerField(default=4)
    four_avg = models.IntegerField(default=0)
    
    five_times_table = models.IntegerField(default=5)
    five_avg = models.IntegerField(default=0)
    
    six_times_table = models.IntegerField(default=6)
    six_avg = models.IntegerField(default=0)
    
    seven_times_table = models.IntegerField(default=7)
    seven_avg = models.IntegerField(default=0)
    
    eight_times_table = models.IntegerField(default=8)
    eight_avg = models.IntegerField(default=0)
    
    nine_times_table = models.IntegerField(default=9)
    nine_avg = models.IntegerField(default=0)
    
    ten_times_table = models.IntegerField(default=10)
    ten_avg = models.IntegerField(default=0)

    eleven_times_table = models.IntegerField(default=11)
    eleven_avg = models.IntegerField(default=0)

    twelve_times_table = models.IntegerField(default=12)
    twelve_avg = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.owner.username}'


class Question(models.Model):
    """Represents a question within a quiz"""
    times_table = models.ForeignKey(TimesTable, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=200)
    option_1 = models.IntegerField()
    option_2 = models.IntegerField()
    option_3 = models.IntegerField()
    option_4 = models.IntegerField()
    answer = models.IntegerField()
    
    def __str__(self):
        return self.question