from django import forms
from .models import UserProfile, Course, Team

class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.filter(is_student=True),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Team
        fields = ["name", "course", "members"]

    def __init__(self, *args, **kwargs):
        course = kwargs.pop("course", None)  # Get the course passed from the view
        super().__init__(*args, **kwargs)
        if course:
            self.fields["members"].queryset = course.students.all()  # Filter students by course