from main_quiz.models import TimesTable, Question
from django.core.management.base import BaseCommand
from django.utils import timezone 

class Command(BaseCommand):
	help = 'Generate times table questions from 1 to 12 times tables'
	def handle(self, *args, **kwargs):
		for times_table in range(1, 13):
			current_times_table = TimesTable.objects.create(times_table=times_table)
			for factor in range(1, 13):
				answer = factor * times_table
				question_text = f"What is {times_table} * {factor}?"
				new_question = Question.objects.create(times_table=current_times_table, question_text=question_text, answer=answer)	
		self.stdout.write("Finished generating questions.")
	
