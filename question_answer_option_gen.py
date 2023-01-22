from main_quiz.models import TimesTable, Question
import random 

def gen_options(answer):
	options = [random.randint(1, 145) for i in range(4) if random.randint(1, 145) not in [answer]]
	options.append(answer)
	random_pos = random.randint(0, 3)
	options.insert(random_pos, answer)
	return options

for i in range(1, 13):
	current_times_table = TimesTable.objects.get(id=i)
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
	
