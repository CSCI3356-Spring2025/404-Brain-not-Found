from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, ProfessorProfile, StudentProfile, Course, Team, Assessment, Question, PredefinedQuestion, QuestionResponse, SemesterType, CourseInvitation
from django.http import JsonResponse
from .forms import TeamForm, AssessmentForm, QuestionForm, QuestionFormSet, QuestionResponseForm, EvaluateStudentForm, StudentInvitationForm
from django.forms import modelformset_factory
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

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
        #student_profile = StudentProfile.objects.get(user=request.user)
        student_profile, created = StudentProfile.objects.get_or_create(user=request.user)

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

    # changed to include ProfessorProfile
def assessment_summary(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    questions = Question.objects.filter(assessment=assessment).order_by('order')
    question_responses = QuestionResponse.objects.filter(assessment=assessment)
    
    try:
        professor_profile = ProfessorProfile.objects.get(user=request.user)
    except ProfessorProfile.DoesNotExist:   
        return redirect(student_dashboard)

    if assessment.professor != professor_profile:   # returns to dash if assessment isn't prof's
        return redirect("professor_dashboard")  

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
    current_student = get_object_or_404(StudentProfile, user=request.user)

    student_team = None
    for course in assessment.course.all():
        try:
            team = Team.objects.get(
                members=current_student,
                course=course
            )
            student_team = team
            break 
        except Team.DoesNotExist:
            continue
        except Team.MultipleObjectsReturned:
            student_team = Team.objects.filter(members=current_student, course=course).first()
            break
    team_members = []
    if student_team:
        team_members = StudentProfile.objects.filter(teams=student_team)

    responses_by_q = []
    for question in questions:
        if question.question_type == 'open':
            responses = question_responses.filter(question=question, evaluated_student=current_student)
            sorted_responses = sorted(
                [r.answer_text for r in responses],
                key=lambda text: text.strip().split()[0].lower() if text.strip() else ''
            )
            print(responses)
            print(sorted_responses)
            responses_by_q.append({'question': question, 'type': 'open', 'responses': sorted_responses})
        else:
            likert_values_class = question_responses.filter(question=question, answer_likert__isnull=False).values_list('answer_likert', flat=True)
            if likert_values_class:
                avg_class = sum(likert_values_class) / len(likert_values_class)
            else:
                avg_class = None
            likert_values_student = question_responses.filter(question=question, evaluated_student=current_student, answer_likert__isnull=False).values_list('answer_likert', flat=True)
            if likert_values_student:
                avg_student = sum(likert_values_student) / len(likert_values_student)
            else:
                avg_student = None
            avg_team = None
            team_name = None
            if student_team:
                likert_values_team = question_responses.filter(question=question, evaluated_student__in=list(team_members) + [current_student], answer_likert__isnull=False).values_list('answer_likert', flat=True)
                if likert_values_team:
                    avg_team = sum(likert_values_team) / len(likert_values_team)
                    team_name = student_team.name

            responses_by_q.append({'question': question, 'type': 'likert', 'average_class': avg_class, 'average_student': avg_student, 'average_team': avg_team, 'team_name': team_name})


 
    context = {
        'user': request.user, 
        'assessment': assessment,
        'responses_by_question': responses_by_q
    }
    return render(request, 'PeerConnect/student_results.html', context)

def create(request):
    #students = UserProfile.objects.filter(is_student=True)
    students = StudentProfile.objects.all()
    professor = get_object_or_404(ProfessorProfile, user=request.user)
    courses = Course.objects.filter(professor=professor)
    active_tab = request.GET.get('tab', 'teams')

    course_id = request.GET.get("course_id")
    selected_course = None
    teams = None
    form = None
    invitations = None
    assessments = None
    if course_id:
        selected_course = get_object_or_404(Course, id=course_id)
        form = TeamForm(course=selected_course)
        teams = Team.objects.filter(course=selected_course)
        invitations = CourseInvitation.objects.filter(course=selected_course)
        assessments = Assessment.objects.filter(course=selected_course)
    else:
        assessments = Assessment.objects.filter(professor=professor)
        
    return render(request, "PeerConnect/create.html", {'professor': professor, 'students': students, 'courses': courses, 'selected_course': selected_course, 'form': form, 'teams': teams, 'SemesterType': SemesterType, 'active_tab': active_tab, 'invitations': invitations, 'assessments': assessments})

    # changed to include StudentProfile
def course_form(request):
    professor = get_object_or_404(ProfessorProfile, user=request.user)
    students = StudentProfile.objects.all()
    return render(request, "PeerConnect/course_form.html", {
        'professor': professor,
        'students': students,
        'SemesterType': SemesterType
    })

def landing_page(request):
    return render(request, "PeerConnect/landingpage.html", {})

    #updated to use studentProfile
@login_required
def professor_dashboard(request):
    try:
        professor = get_object_or_404(ProfessorProfile, user=request.user)
    except ProfessorProfile.DoesNotExist:
        return redirect("student_dashboard") 
    courses = Course.objects.filter(professor=professor)
    #students = StudentProfile.objects.filter(is_student=True) #changed from UserProfile
    #students = StudentProfile.objects.filter(courses_enrolled__in=courses)
    students = StudentProfile.objects.filter()
    assessments = Assessment.objects.filter(professor=professor)
    return render(request, "PeerConnect/professor_dashboard.html", {'courses': courses, 'students': students, 'assessments': assessments, 'SemesterType': SemesterType})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/student_dashboard/') 
    return render(request, "signup.html")

@login_required
def create_course(request):
    if request.method == "POST":
        name = request.POST.get("name")
        student_ids = request.POST.getlist("students")
        semester = request.POST.get('semester')
        year = request.POST.get('year')

        professor = get_object_or_404(ProfessorProfile, user=request.user)
        course = Course.objects.create(name=name, professor=professor, semester=semester, year=int(year))
        students = StudentProfile.objects.filter(id__in=student_ids)
        course.students.set(students)
    
        base_url = reverse('create')
        url_with_course_id = f"{base_url}?course_id={course.id}"
        return redirect(url_with_course_id)
    return JsonResponse({"error": "Invalid request"}, status=400)

# def edit_course(request, course_id):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         student_ids = request.POST.getlist("students")
#         semester = request.POST.get('semester')
#         year = request.POST.get('year')

#         professor = get_object_or_404(ProfessorProfile, user=request.user)
#         students = StudentProfile.objects.filter(id__in=student_ids)
#         course = get_object_or_404(Course, id=course_id)
#         students = UserProfile.objects.filter(student=True)
#         course.students.set(students)
    
#         return render(request, 'course_form.html', {
#         'students': students,
#         'edit_mode': True,
#         'course': course
#     })
#     return JsonResponse({"error": "Invalid request"}, status=400)

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect("/create/")

def course_roster(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = StudentInvitationForm(request.POST)

        if form.is_valid():
            #student_name = form.cleaned_data['student_name']
            #student_email = form.cleaned_data['student_email']
            invitations_text = form.cleaned_data['invitations']
            student_pairs = invitations_text.splitlines()  # Split by new line

            for pair in student_pairs:
                parts = pair.split(',')
                if len(parts) == 2:
                    name = parts[0].strip()
                    email = parts[1].strip()
                    
                    invitation = CourseInvitation(course=course, email=email)
                    invitation.save()

                    token_url = f"{request.build_absolute_uri('/accept_invite/')}{course.id}/{email}"  # Adjust URL as needed
                    
                    send_mail(
                        "Course Invitation", #message name
                        f"Hello {name},\n\nYou have been invited to join the course: {course.name}. Click the link to accept: {token_url}", #message
                        settings.EMAIL_HOST_USER,  # Host email address
                        [email],  # Student's email
                        fail_silently=False,  # Raise errors if sending fails
                    )
                    # invitation = CourseInvitation.objects.create(
                    #     course=course,
                    #     email=student_email,
                    #     #token=token
                    # )
            return redirect("course_roster", course_id=course.id)

    else:
        form = StudentInvitationForm()

    invitations = CourseInvitation.objects.filter(course=course)
    return render(request, "PeerConnect/course_roster.html", {'course': course}) #, 'form': form, 'invitations': invitations})


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
    professor = get_object_or_404(ProfessorProfile, user=request.user)
    
    # Get the number of questions from either the session or the POST data
    if "add_question" in request.POST:
        num_questions = int(request.POST.get('form_count', 1)) + 1
    else:
        num_questions = int(request.session.get('questions', 1))
    
    # Store the updated count in the session
    request.session['questions'] = num_questions
    
    # Create the formset with the appropriate number of extra forms
    QuestionFormSetDynamic = modelformset_factory(
        Question, 
        form=QuestionForm, 
        extra=num_questions, 
        can_delete=True
    )
    
    if request.method == "POST":
        form = AssessmentForm(request.POST)
        
        if "add_question" in request.POST:
            # Create a new formset with one more form
            formset = QuestionFormSetDynamic(queryset=Question.objects.none())
            
            # Pre-fill the form with any existing data
            # This preserves data for existing questions
            for i, subform in enumerate(formset):
                prefix = f'form-{i}'
                for field_name in subform.fields:
                    field_key = f'{prefix}-{field_name}'
                    if field_key in request.POST and i < num_questions - 1:
                        subform.initial[field_name] = request.POST.get(field_key)
            
            context = {
                'form': form,  # Keep the entered assessment data
                'formset': formset,
                'courses': Course.objects.filter(professor=professor),
                'form_count': num_questions
            }
            return render(request, "PeerConnect/create_assessment.html", context)
        
        # For normal form submission
        formset = QuestionFormSetDynamic(request.POST, queryset=Question.objects.none())
        
        if form.is_valid() and formset.is_valid():
            assessment = form.save(commit=False)
            assessment.professor = professor
            assessment.save()
            form.save_m2m()
            
            questions = formset.save(commit=False)
            for index, question in enumerate(questions):
                question.assessment = assessment
                question.order = index + 1
                question.save()
            formset.save_m2m()
            
            # Reset the session
            request.session['questions'] = 1
            return redirect("professor_dashboard")
    else:
        form = AssessmentForm()
        formset = QuestionFormSetDynamic(queryset=Question.objects.none())
    
    context = {
        'form': form,
        'formset': formset,
        'courses': Course.objects.filter(professor=professor),
        'form_count': num_questions
    }
    return render(request, "PeerConnect/create_assessment.html", context)


@login_required
def view_assessment(request, assessment_id):
    professor = get_object_or_404(ProfessorProfile, user=request.user)
    assessment = get_object_or_404(Assessment, id=assessment_id)

    if assessment.professor == professor:
        extra_forms = int(request.GET.get("extra", 0)) 
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
    student = get_object_or_404(StudentProfile, user=request.user)
    questions = assessment.questions.all()
    
    # Get the course for the assessment
    course = assessment.course.first()  # Assuming the assessment is associated with at least one course
    
    # Initialize the student selection form
    evaluated_student_form = EvaluateStudentForm(course=course)
    
    # Handle the case where a student is selected or form is submitted
    evaluated_student_id = request.POST.get('evaluated_student') or request.GET.get('evaluated_student')
    evaluated_student = None
    
    if evaluated_student_id:
        evaluated_student = get_object_or_404(StudentProfile, id=evaluated_student_id)
        
        # Get or create responses for this specific evaluation
        for question in questions:
            QuestionResponse.objects.get_or_create(
                student=student,  # The student filling out the form
                evaluated_student=evaluated_student,  # The student being evaluated
                assessment=assessment,
                question=question
            )
    
    if request.method == "POST" and 'submit_responses' in request.POST:
        # This handles the actual form submission
        formset = QuestionResponseFormSet(
            request.POST,
            queryset=QuestionResponse.objects.filter(
                student=student, 
                assessment=assessment,
                evaluated_student=evaluated_student
            )
        )

        if formset.is_valid():
            responses = formset.save(commit=False)
            for response in responses:
                response.student = student
                response.evaluated_student = evaluated_student
                response.assessment = assessment
                response.save()
            
            messages.success(request, f"Assessment submitted for {evaluated_student.user.get_full_name()}")
            return redirect('/student_dashboard/')
        else:
            print("Formset errors:", formset.errors)
    else:
        # If a student is selected, show the form pre-filled with any existing responses
        if evaluated_student:
            formset = QuestionResponseFormSet(
                queryset=QuestionResponse.objects.filter(
                    student=student, 
                    assessment=assessment,
                    evaluated_student=evaluated_student
                )
            )
        else:
            # No student selected yet, just render the selection form
            formset = None

    return render(request, "PeerConnect/submit_assessment.html", {
        "assessment": assessment, 
        "formset": formset,
        "evaluated_student_form": evaluated_student_form,
        "evaluated_student": evaluated_student
    })


@login_required
def publish_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    professor = get_object_or_404(ProfessorProfile, user=request.user)

    if assessment.professor != professor:
        return redirect('unauthorized')

    print(f"Assessment {assessment.id}. Published: {assessment.published}")
    
    assessment.published = True
    assessment.save()
    
    print(f"Assessment {assessment.id}. Published: {assessment.published}")

    return redirect('assessment_summary', assessment_id=assessment.id)
