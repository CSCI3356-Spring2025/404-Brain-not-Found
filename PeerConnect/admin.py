from django.contrib import admin
from .models import UserProfile, Course, Team, Assessment, Question

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Team)


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1 

class AssessmentAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Question)