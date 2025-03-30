from django import forms
from .models import UserProfile, Team, Assessment

class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.none(),  # Default to empty, will be set dynamically
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Team
        fields = ["name", "members"]

    def __init__(self, *args, **kwargs):
        course = kwargs.pop("course", None)  # Extract course from kwargs
        super().__init__(*args, **kwargs)

        if course:
            self.course = course  # Store course for later
            self.fields["members"].queryset = course.students.all()

        self.fields["members"].label_from_instance = lambda obj: f"{obj.user.first_name} {obj.user.last_name}"

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ["name", "course", "team", "available_date", "due_date", "self_assessment", "num_questions"]

    def __init__(self, *args, **kwargs):
        course = kwargs.pop("course", None)  # Extract course from kwargs
        super().__init__(*args, **kwargs)

        if course:
            self.fields["name"].label = f"Assessment Name for {course.name}"
            self.fields["available_date"].label = f"Available Date for {course.name}"
            self.fields["due_date"].label = f"Due Date for {course.name}"
        
        self.fields["self_assessment"].label = "Is this a self-assessment?"

        self.fields["num_questions"].label = "Number of Questions"