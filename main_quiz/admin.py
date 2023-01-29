from django.contrib import admin

# Import the TimesTable model that was created
from .models import TimesTable, Question, QuestionOverview

# Allows admin to manage the model through the admin site.
admin.site.register(TimesTable)
admin.site.register(Question)
admin.site.register(QuestionOverview)
