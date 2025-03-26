from django.db import models
from django.contrib.auth.models import User

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
    

class Assessment(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='forms')
    due_date = models.DateTimeField()
    questions = models.TextField()
    
    def __str__(self):
        return f"{self.name} ({self.course.name})"

