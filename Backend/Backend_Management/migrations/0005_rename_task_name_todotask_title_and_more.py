# Generated by Django 5.1.5 on 2025-02-18 06:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend_Management', '0004_studydata_difficulty_level_alter_goal_end_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='todotask',
            old_name='task_name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='todotask',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='todotask',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='todotask',
            name='progress',
        ),
        migrations.RemoveField(
            model_name='todotask',
            name='status',
        ),
        migrations.RemoveField(
            model_name='todotask',
            name='time_estimate',
        ),
        migrations.AddField(
            model_name='todotask',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='todotask',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
