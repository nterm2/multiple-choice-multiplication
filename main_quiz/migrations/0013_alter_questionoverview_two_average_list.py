# Generated by Django 4.1.5 on 2023-02-01 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_quiz', '0012_alter_questionoverview_eight_times_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionoverview',
            name='two_average_list',
            field=models.TextField(default='[]'),
        ),
    ]