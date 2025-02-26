from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# To-Do Model
class ToDoTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Study Data Model
class StudyData(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study_hours = models.FloatField()  # Hours studied
    study_topic = models.CharField(max_length=255)
    study_date = models.DateField()
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Medium')  # Difficulty Level

    def __str__(self):
        return f"{self.study_topic} on {self.study_date}"
    
    @classmethod
    def get_total_study_hours(cls, user, topic):
        """Get total hours studied by the user for a specific topic."""
        return cls.objects.filter(user=user, study_topic=topic).aggregate(total_hours=models.Sum('study_hours'))['total_hours'] or 0
  
# Exam Marks Model
class ExamMarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_data')
    subject = models.CharField(max_length=255)
    exam_date = models.DateField()
    preparation_start_date = models.DateField(blank=True, null=True)
    hours_studied = models.FloatField()
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()

    def __str__(self):
        return f"{self.subject} - {self.exam_date}"

 