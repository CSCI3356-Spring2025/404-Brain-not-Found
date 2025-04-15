from django.contrib import admin
from .models import UserProfile, StudentProfile, ProfessorProfile, Course, Team, Assessment, Question, PredefinedQuestion, QuestionResponse, CourseInvitation
from .forms import AssessmentForm, QuestionForm

# Register your models here.
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # How many empty forms to display

class AssessmentAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_professor', 'is_student'] # displays user and their role
    list_filter = ['is_professor', 'is_student'] # can filter based on prof or student
    search_fields = ['user__username', 'user__email'] # search by name or email

        # saves whether profile is a student or professor
    def save_model(self, request, obj, form, change):
        obj.save() #saves user to database
        if obj.is_student:
                # gets prof profile if existing, deletes it
            deactive_prof = ProfessorProfile.objects.filter(user=obj.user).first()
            if deactive_prof:
                deactive_prof.active = False
                deactive_prof.save()
            
                # save new student or activate deactive Student
            student, created = StudentProfile.objects.get_or_create(user=obj.user)
            student.active = True
            student.save

        elif obj.is_professor:
            deactive_student = StudentProfile.objects.filter(user=obj.user).first()
            if deactive_student:
                deactive_student.active = False
                deactive_student.save()
            
                # save new Prof or activate deactive Prof
            professor, created = ProfessorProfile.objects.get_or_create(user=obj.user)
            professor.active = True
            professor.save
        
        super().save_model(request, obj, form, change)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Course)
admin.site.register(Team)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Question)
admin.site.register(PredefinedQuestion)
admin.site.register(QuestionResponse)
admin.site.register(CourseInvitation)
admin.site.register(StudentProfile)
admin.site.register(ProfessorProfile)
