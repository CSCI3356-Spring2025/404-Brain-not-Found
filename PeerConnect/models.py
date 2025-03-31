from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=True)
    is_professor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courses_taught')
    students = models.ManyToManyField(UserProfile, related_name='courses_enrolled', limit_choices_to={'is_student': True})

    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='teams')
    members = models.ManyToManyField(UserProfile, related_name='teams', limit_choices_to={'is_student': True})
    
    def __str__(self):
        return f"{self.name} ({self.course.name})"
    
class PredefinedQuestion(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
        
class Assessment(models.Model):
    professor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='assessments_created')  # Link to the professor who created the assessment
    name = models.CharField(max_length=255)
    course = models.ManyToManyField(Course, related_name='assessments')  # Many-to-many to allow multiple courses to use the same assessment
    team = models.ManyToManyField(Team, related_name='assessments', blank=True)  # Optional if not tied to a specific team
    available_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default= timezone.now() + timedelta(days=7))
    self_assessment = models.BooleanField(default=False)
    num_questions = models.PositiveIntegerField(default=0)
    

    predefined_questions = models.ManyToManyField(PredefinedQuestion, blank=True)
    
    
    def __str__(self):
        courses_names = ", ".join(course.name for course in self.course.all())
        return f"{self.name} ({courses_names})"

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('likert', 'Likert Scale'),
        ('open', 'Open-Ended'),
    ]
    
    assessment = models.ForeignKey(Assessment, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField()
    question_type = models.CharField(max_length=10, choices = QUESTION_TYPE_CHOICES, default = "open")
    
    def __str__(self):
        return f"{self.get_question_type_display()} Question {self.order}: {self.text[:30]}"
