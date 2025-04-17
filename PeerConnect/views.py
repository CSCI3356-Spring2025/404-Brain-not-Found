from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, ProfessorProfile, StudentProfile, Course, Team, Assessment, Question, PredefinedQuestion, QuestionResponse
from django.http import JsonResponse
from .forms import TeamForm, AssessmentForm, QuestionForm, QuestionFormSet, QuestionResponseForm
from django.forms import modelformset_factory


    #updated to use StudentProfile and Prof profile
def student_dashboard(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    #students = UserProfile.objects.filter(is_student=True)
    # if user_profile.is_professor:
    #     return redirect("professor_dashboard")
    try:
        professor_profile = ProfessorProfile.objects.get(user=request.user)
        return redirect("professor_dashboard")
    except ProfessorProfile.DoesNotExist:
        user_type = "Student"
        student_profile = StudentProfile.objects.get(user=request.user)
        courses = student_profile.courses_enrolled.all()
        teams = student_profile.teams.all()
        assessments = Assessment.objects.filter(course__in=courses)

        return render(request, "PeerConnect/student_dashboard.html", {
            'user': request.user, 
            'type': user_type, 
            'courses': courses, 
            'teams': teams, 
            'assessments': assessments
        })

def peer_answer_qual(request):
    return render(request, "PeerConnect/peer_answer_qual.html", {})

def peer_answer_quant(request):
    return render(request, "PeerConnect/peer_answer_quant.html", {})

def assessment_summary(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    questions = Question.objects.filter(assessment=assessment).order_by('order')
    question_responses = QuestionResponse.objects.filter(assessment=assessment)
    if assessment.professor != request.user.userprofile:
        return redirect("professor_dashboard")  # Prevent unauthorized access
    context = {
        'assessment': assessment,
        'questions': questions,
        'question_responses': question_responses
    }
    return render(request, 'PeerConnect/peer_assessment_summary.html', context)

def student_results(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    questions = Question.objects.filter(assessment=assessment).order_by('order')
    question_responses = QuestionResponse.objects.filter(assessment=assessment)
    responses_by_q = []
    for question in questions:
        if question.question_type == 'open':
            responses = question_responses.filter(question=question)
            sorted_responses = sorted(
                [r.answer_text for r in responses],
                key=lambda text: text.strip().split()[0].lower() if text.strip() else ''
            )
            print(responses)
            print(sorted_responses)
            responses_by_q.append({'question': question, 'type': 'open', 'responses': sorted_responses})
        else:
            likert_values = question_responses.filter(question=question, answer_likert__isnull=False).values_list('answer_likert', flat=True)
            if likert_values:
                avg = sum(likert_values) / len(likert_values)
            else:
                avg = None
            responses_by_q.append({'question': question, 'type': 'likert', 'average': avg})


 
    context = {
        'assessment': assessment,
        'responses_by_question': responses_by_q
    }
    return render(request, 'PeerConnect/student_results.html', context)

def create(request):
    students = UserProfile.objects.filter(is_student=True)
    professor = get_object_or_404(UserProfile, user=request.user)
    courses = Course.objects.filter(professor=professor)


    course_id = request.GET.get("course_id")
    selected_course = None
    teams = None
    form = None
    if course_id:
        selected_course = get_object_or_404(Course, id=course_id)
        form = TeamForm(course=selected_course)
        teams = Team.objects.filter(course=selected_course)
    return render(request, "PeerConnect/create.html", {'professor': request.user, 'students': students, 'courses': courses, 'selected_course': selected_course, 'form': form, 'teams': teams})

def course_form(request):
    students = UserProfile.objects.filter(is_student=True)
    return render(request, "PeerConnect/course_form.html", {'professor': request.user, 'students': students})

def landing_page(request):
    return render(request, "PeerConnect/landingpage.html", {})

    #updated to use studentProfile
def professor_dashboard(request):
    try:
        professor = get_object_or_404(ProfessorProfile, user=request.user)
    except ProfessorProfile.DoesNotExist:
        return redirect("student_dashboard") 
    courses = Course.objects.filter(professor=professor)
    #students = StudentProfile.objects.filter(is_student=True) #changed from UserProfile
    students = StudentProfile.objects.filter(courses_enrolled__in=courses)
    assessments = Assessment.objects.filter(professor=professor)
    return render(request, "PeerConnect/professor_dashboard.html", {'courses': courses, 'students': students, 'assessments': assessments})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/student_dashboard/') 
    return render(request, "signup.html")

@login_required
def create_course(request):
    if request.method == "POST":
        name = request.POST.get("name")
        student_ids = request.POST.getlist("students")
        professor = get_object_or_404(UserProfile, user=request.user)
        course = Course.objects.create(name=name, professor=professor)
        students = UserProfile.objects.filter(id__in=student_ids, is_student=True)
        course.students.set(students)
    
        return redirect("/create/")
    return JsonResponse({"error": "Invalid request"}, status=400)

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect("/create/")

def render_create_team(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()  
    form = TeamForm(course=course)
    teams = Team.objects.filter(course=course)
    return render(request, "PeerConnect/create_team.html", {'professor': request.user, 'students': students, 'course': course, 'form': form, 'teams': teams}) 


@login_required
def create_team(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = TeamForm(request.POST, course=course) 
        if form.is_valid():
            team = form.save(commit=False)
            team.course = course  
            team.save() 
            form.save_m2m()
            return redirect("create")
        return JsonResponse({"errors": form.errors}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

def delete_team(request,  team_id):
    team = get_object_or_404(Team, id=team_id)
    team.delete()
    return redirect("/create/")

@login_required
def dashboard_redirect(request):
    return redirect('/dashboard/')  # Change this if needed

@login_required
def create_assessment(request):
    professor = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST" :

        form = AssessmentForm(request.POST)
        if form.is_valid() :
            assessment = form.save(commit=False)
            assessment.professor = professor
            assessment.save()
            form.save_m2m()
            #formset.instance = assessment

            formset = QuestionFormSet(request.POST, instance=assessment)
            print(request.POST.dict())
            if  formset.is_valid():
                questions = formset.save(commit=False)
                for index, question in enumerate(questions):
                    question.assessment = assessment
                    question.order = index + 1
                    question.save()
                formset.save_m2m()
            else:
                # If question formset has errors, re-render with errors
                return render(request, "PeerConnect/create_assessment.html", {
                    'form': form,
                    'formset': formset,
                    'courses': Course.objects.filter(professor=professor)
                })
            return redirect("professor_dashboard")

        else:
            formset = QuestionFormSet(request.POST)
    
    else:
        form = AssessmentForm()
        formset = QuestionFormSet()

    context = {
        'form': form,
        'formset': formset,
        'courses': Course.objects.filter(professor=professor)
    }
    return render(request, "PeerConnect/create_assessment.html", context)

    # #professor = get_object_or_404(UserProfile, user=request.user)
    # if request.method == "POST" and form.is_valid():
    #     professor = get_object_or_404(UserProfile, user=request.user)
    #     assessment = form.save(commit=False)
    #     assessment.professor = professor 
    #     assessment.save()
    #     form.save_m2m()
        
    #     assessment.course.set(form.cleaned_data['course'])
    
    #     if form.cleaned_data.get('teams'):
    #         assessment.teams.set(form.cleaned_data['teams'])

    #     num_questions = form.cleaned_data.get('num_questions', 0)
    #     # for i in range(num_questions):
    #     #     question_text = form.cleaned_data.get(f"question_{i}_text")
    #     #     question_type_id = form.cleaned_data.get(f"question_{i}_type")

    #     #     if question_text and question_type:
    #     #         question_type = Question.objects.get(id=question_type_id)
    #     #         question = Question.objects.create(
    #     #             assessment=assessment,
    #     #             text=question_text,
    #     #             order=i + 1,
    #     #             question_type=question_type_id
    #     #         )
    #     return redirect("professor_dashboard")
    
    # #professor = get_object_or_404(UserProfile, user=request.user)  # Fetch professor for filtering courses

    # context = {
    #     'form': form,
    #     'courses': Course.objects.filter(professor=professor)
    # }

    # return render(request, "PeerConnect/create_assessment.html", context)

@login_required
def view_assessment(request, assessment_id):
    professor = get_object_or_404(UserProfile, user=request.user)
    assessment = get_object_or_404(Assessment, id=assessment_id)

    if assessment.professor == professor:
        questions = Question.objects.filter(assessment=assessment).order_by('order')
        QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=0, can_delete=True)

        if request.method == 'POST':
            form = AssessmentForm(request.POST, instance=assessment)
            formset = QuestionFormSet(request.POST, queryset=questions)

            if form.is_valid() and formset.is_valid():
                form.save()
                updated_questions = formset.save(commit=False)

                for index, question in enumerate(updated_questions):
                    question.assessment = assessment
                    question.order = index + 1
                    question.save()

                formset.save_m2m()
                return redirect("professor_dashboard")
            else:
                return render(request, "PeerConnect/view_assessment.html", {
                    'assessment': assessment,
                    'form': form,
                    'formset': formset,
                    'courses': Course.objects.filter(professor=professor)
                })

        else:
            form = AssessmentForm(instance=assessment)
            formset = QuestionFormSet(queryset=questions)

        return render(request, "PeerConnect/view_assessment.html", {
            'assessment': assessment,
            'form': form,
            'formset': formset,
            'courses': Course.objects.filter(professor=professor)
        })

QuestionResponseFormSet = modelformset_factory(QuestionResponse, form=QuestionResponseForm, extra=0)

def submit_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    student = request.user.userprofile
    questions = assessment.questions.all()

    # Ensure that QuestionResponse objects are created if they don't exist
    for question in questions:
        QuestionResponse.objects.get_or_create(
            student=student,
            assessment=assessment,
            question=question
        )

    if request.method == "POST":
        # Get the formset with existing responses (if any)
        formset = QuestionResponseFormSet(
            request.POST,
            queryset=QuestionResponse.objects.filter(student=student, assessment=assessment)
        )

        if formset.is_valid():
            responses = formset.save(commit=False)
            for response, question in zip(responses, questions):
                response.student = student
                response.assessment = assessment
                response.question = question  # Ensure each response is linked to a question
                response.save()
            return redirect('/student_dashboard/')
        else:
            print("Formset errors:", formset.errors)  # Debug errors
            print("POST data:", request.POST)  # Check if id is missing
    else:
        # Prefill responses if student has already attempted some
        formset = QuestionResponseFormSet(queryset=QuestionResponse.objects.filter(student=student, assessment=assessment))

    return render(request, "PeerConnect/submit_assessment.html", {"assessment": assessment, "formset": formset})

@login_required
def publish_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)

    if assessment.professor != request.user.userprofile:
        return redirect('unauthorized')

    print(f"Assessment {assessment.id}. Published: {assessment.published}")
    
    assessment.published = True
    assessment.save()
    
    print(f"Assessment {assessment.id}. Published: {assessment.published}")

    return redirect('assessment_summary', assessment_id=assessment.id)
