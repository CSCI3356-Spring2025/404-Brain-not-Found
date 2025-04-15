from django import forms
from .models import UserProfile, Team, Assessment, PredefinedQuestion, Question, QuestionResponse
from django.utils import timezone
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe
from django.forms import modelformset_factory


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
    #available_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label="Available Date", initial=timezone.now)
    #due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label="Due Date", initial=timezone.now)
    available_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
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
        # num_questions = self.initial.get("num_questions", 0)
        # for i in range(num_questions):
        #     self.fields[f"question_{i}_text"] = forms.CharField(max_length=255, label=f"Question {i+1}")
        #     self.fields[f"question_{i}_type"] = forms.ChoiceField(choices=Question.QUESTION_TYPE_CHOICES, label=f"Question {i+1} Type")
    

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type']

QuestionFormSet = inlineformset_factory(
    Assessment,
    Question,
    form=QuestionForm,
    fields=['text', 'question_type'],
    extra=1,
    can_delete=True
)

class StarRatingWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if not value:
            value = 0
        output = '<div class="star-rating">'
        for i in range(5, 0, -1):
            checked = 'checked' if str(value) == str(i) else ''
            output += f'''
                <input type="radio" id="{name}_{i}" name="{name}" value="{i}" {checked}>
                <label for="{name}_{i}">&#9733;</label>
            '''
        output += '</div>'
        return mark_safe(output)

class QuestionResponseForm(forms.ModelForm):
    class Meta:
        model = QuestionResponse
        fields = ['id', 'answer_text', 'answer_likert']
        widgets = {
            'answer_likert': StarRatingWidget()
        }


QuestionResponseFormSet = modelformset_factory(
    QuestionResponse,
    form=QuestionResponseForm,
    extra=0,
    fields=['id', 'answer_text', 'answer_likert'] 
)

    # professor can send invites to students
class InviteStudentsForm(forms.Form):
    emails = forms.CharField(widget=forms.Textarea, help_text="Enter one email per line.")