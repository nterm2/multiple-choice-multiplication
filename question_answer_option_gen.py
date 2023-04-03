from main_quiz.models import TimesTable, Question
import random 
# Before running this script, run python manage.py migrate
# Then, create superuser, and from the admin panel, manually add the 1 times tables all the way to the 12 times table within the timetable model.
# Now execute the script, and the times tables should be populated

def gen_options(answer):
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

for i in range(1, 13):
	current_times_table = TimesTable.objects.get(times_table=i)
	times_table = current_times_table.times_table
	for i in range(1, 13):
		answer = i * times_table
		question = f"What is {times_table} * {i}?"
		options = gen_options(answer)
		option_1 = options[0]
		option_2 = options[1]
		option_3 = options[2]
		option_4 = options[3]	
		
		new_question = Question.objects.create(times_table=current_times_table, question=question, option_1=option_1, option_2=option_2, option_3=option_3, option_4=option_4, answer=answer)	
	
