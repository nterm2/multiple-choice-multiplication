from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

# Allows admin to manage the model through the admin site.
app_models = apps.get_app_config('main_quiz').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass