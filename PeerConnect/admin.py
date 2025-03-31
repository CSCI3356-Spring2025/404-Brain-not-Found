from django.contrib import admin
from .models import UserProfile, Course, Team, Assessment, Question, PredefinedQuestion

# Register your models here.



class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1 

class AssessmentAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Team)
admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(PredefinedQuestion)