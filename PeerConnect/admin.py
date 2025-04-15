from django.contrib import admin
from .models import UserProfile, StudentProfile, ProfessorProfile, Course, Team, Assessment, Question, PredefinedQuestion, QuestionResponse, CourseInvitation
from .forms import AssessmentForm, QuestionForm

# Register your models here.
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # How many empty forms to display

class AssessmentAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Team)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Question)
admin.site.register(PredefinedQuestion)
admin.site.register(QuestionResponse)
admin.site.register(CourseInvitation)
admin.site.register(StudentProfile)
admin.site.register(ProfessorProfile)
