from django.db import models

class TimesTable(models.Model):
    """Represents the values associated for a given times table."""
    times_table = models.IntegerField()
    average_percentage = models.IntegerField()

    def __str__(self):
        """Return a string representation of the TimesTable model"""
        return f'Times Table: {self.times_table} Average Percentage: {self.average_percentage}%'

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