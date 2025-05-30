from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=True)
    is_professor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class ProfessorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class SemesterType(models.TextChoices):
    SPRING = 'spring', 'Spring'
    FALL = 'fall', 'Fall'
    SUMMER = 'summer', 'Summer'
    WINTER = 'winter', 'Winter'


class Course(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.CASCADE, related_name='courses_taught')
    students = models.ManyToManyField(StudentProfile, related_name='courses_enrolled')
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)], null=True, blank=True)
    semester = models.CharField(max_length=10, choices = SemesterType.choices, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='teams')
    members = models.ManyToManyField(StudentProfile, related_name='teams')
    
    def __str__(self):
        return f"{self.name} ({self.course.name})"
        
class Assessment(models.Model):
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.CASCADE, related_name='assessments_created')  # Link to the professor who created the assessment
    name = models.CharField(max_length=255)
    course = models.ManyToManyField(Course, related_name='assessments')  # Many-to-many to allow multiple courses to use the same assessment
    team = models.ManyToManyField(Team, related_name='assessments', blank=True)  # Optional if not tied to a specific team
    available_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default= timezone.now() + timedelta(days=7))
    self_assessment = models.BooleanField(default=False)
    
        # tracks whether results are published
    published = models.BooleanField(default=False)
        
        # tracks whether available reminder sent 
    available_reminder_sent = models.BooleanField(default=False)

        # tracks whether due soon reminder sent 
    due_soon_reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        courses_names = ", ".join(course.name for course in self.course.all())
        return f"{self.name} ({courses_names})"


class QuestionType(models.TextChoices):
    OPEN = 'open', 'Open-Ended'
    LIKERT = 'likert', 'Likert Scale'

class Question(models.Model):
    assessment = models.ForeignKey(Assessment, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    question_type = models.CharField(max_length=10, choices = QuestionType.choices, default = QuestionType.OPEN)
    
    def __str__(self):
        return f"{self.get_question_type_display()} Question {self.order}: {self.text[:30]}"

class QuestionResponse(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='responses')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='responses') #is this needed w question?
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    answer_text = models.TextField(blank=True, null=True)
    answer_likert = models.IntegerField(blank=True, null=True)
    #submitted_at = models.DateTimeField(auto_now_add=True)
    
    evaluated_student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='evaluations_received', null=True)


    def __str__(self):
        return f"Response by {self.student} for {self.question}"

#track course invitations
class CourseInvitation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='invitations')
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False) #makes email invite individualized
    accepted = models.BooleanField(default=False)

    