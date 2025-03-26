from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Course, Team
from django.http import JsonResponse
from .forms import TeamForm

def student_dashboard(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if user_profile.is_professor:
        user_type = "Professor"
        return render(request, "PeerConnect/professor_dashboard.html", {'user': request.user, 'type': user_type})
    else:
        user_type = "Student"
    return render(request, "PeerConnect/student_dashboard.html", {'user': request.user, 'type': user_type})

def peer_answer_qual(request):
    return render(request, "PeerConnect/peer_answer_qual.html", {})

def peer_answer_quant(request):
    return render(request, "PeerConnect/peer_answer_quant.html", {})

def create(request):
    students = UserProfile.objects.filter(is_student=True)
    professor = get_object_or_404(UserProfile, user=request.user)
    courses = Course.objects.filter(professor=professor)

    selected_course = None  # Default to None

    if "selected_course_id" in request.GET:
        selected_course = Course.objects.filter(id=request.GET["selected_course_id"]).first()

    print(courses)
    return render(request, "PeerConnect/create.html", {'professor': request.user, 'students': students, 'courses': courses, 'selected_course': selected_course})

def course_form(request):
    students = UserProfile.objects.filter(is_student=True)
    print("Students: ")
    print(students)
    return render(request, "PeerConnect/course_form.html", {'professor': request.user, 'students': students})

def landing_page(request):
    return render(request, "PeerConnect/landingpage.html", {})

def professor_dashboard(request):
    return render(request, "PeerConnect/professor_dashboard.html", {})

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

def render_create_team(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()  
    form = TeamForm(course=course)
    return render(request, "PeerConnect/create_team.html", {'professor': request.user, 'students': students, 'course': course, 'form': form}) 


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
            return redirect("create_team", course_id=course.id)
        return JsonResponse({"errors": form.errors}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def dashboard_redirect(request):
    return redirect('/dashboard/')  # Change this if needed