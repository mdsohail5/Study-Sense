# Generated by Django 5.1.5 on 2025-02-17 04:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend_Management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamMarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('exam_date', models.DateField()),
                ('hours_studied', models.FloatField()),
                ('marks_obtained', models.FloatField()),
                ('total_marks', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_data', to='Backend_Management.user')),
            ],
        ),
        migrations.CreateModel(
            name='StudyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_hours', models.FloatField()),
                ('study_topic', models.CharField(max_length=255)),
                ('study_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Backend_Management.user')),
            ],
        ),
    ]
