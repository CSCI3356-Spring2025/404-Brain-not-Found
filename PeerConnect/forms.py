from django import forms
from .models import UserProfile, Team, Assessment, PredefinedQuestion, Question
from django.utils import timezone




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
    predefined_questions = forms.ModelMultipleChoiceField(
        queryset=PredefinedQuestion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required = False,
        label = "Common Questions"
    )
    available_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label="Available Date", initial=timezone.now)
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label="Due Date", initial=timezone.now)
    # available_date = forms.DateTimeField(
    #     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    #     input_formats=['%Y-%m-%dT%H:%M']
    # )
    # due_date = forms.DateTimeField(
    #     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    #     input_formats=['%Y-%m-%dT%H:%M']
    # )
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
        num_questions = self.initial.get("num_questions", 0)
        for i in range(num_questions):
            self.fields[f"question_{i}_text"] = forms.CharField(max_length=255, label=f"Question {i+1}")
            self.fields[f"question_{i}_type"] = forms.ModelChoiceField(queryset=QuestionType.objects.all(), label=f"Question {i+1} Type")
    
    def save(self, commit=True):
        assessment = super().save(commit=False)
        if commit:
            assessment.save()
            self.save_questions(assessment)
        return assessment

    def save_questions(self, assessment):
        num_questions = len(self.cleaned.data.get('num_questions'))
        for i in range(num_questions):
            text = self.cleaned_data.get(f"question_{i}_text")
            question_type = self.cleaned_data.get(f"question_{i}_type")

            question = Question.objects.create(
                assessment=assessment,
                text=text,
                order=i + 1,
                question_type=question_type
            )
            question.save()

