from django import forms
from .models import UserProfile, Team

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
