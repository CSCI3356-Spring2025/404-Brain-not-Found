from django.contrib import admin
from .models import UserProfile, Course, Team, Assessment, Question, PredefinedQuestion
from .forms import AssessmentForm

# Register your models here.

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1 

class AssessmentAdmin(admin.ModelAdmin):
    form = AssessmentForm
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'order', 'question_type', 'text')
    list_filter = ('question_type',)
    search_fields = ('text',)

admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Team)
admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(PredefinedQuestion)