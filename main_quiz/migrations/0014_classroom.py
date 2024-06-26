# Generated by Django 5.0.4 on 2024-05-26 07:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_studentprofile_teacherprofile'),
        ('main_quiz', '0013_alter_questionoverview_two_average_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('classroom_name', models.CharField(max_length=100)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.teacherprofile')),
            ],
        ),
    ]
