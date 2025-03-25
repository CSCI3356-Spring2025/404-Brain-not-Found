from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Course, Team
from django.http import JsonResponse

# Create your views here.
def student_dashboard(request):
    #user_profile = get_object_or_404(UserProfile, user=request.user)
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

def render_create_course(request):
    students = UserProfile.objects.filter(is_student=True)
    return render(request, "PeerConnect/create.html", {'professor': request.user, 'students': students})

def render_create_team(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()  
    #update this with the correct html page once that's created
    return render(request, "PeerConnect/create.html", {'professor': request.user, 'students': students}) 

def landing_page(request):
    return render(request, "PeerConnect/landingpage.html", {})

def professor_dashboard(request):
    return render(request, "PeerConnect/professor_dashboard.html", {})

def signup_view(request):
    # Check if user is already signed up
    if request.user.is_authenticated:
        return redirect('/student_dashboard/')  # Change this to your actual dashboard URL
    return render(request, "signup.html")

@login_required
def create_course(request):
    if request.method == "POST":
        name = request.POST.get("name")
        student_ids = request.POST.getlist("students")
        professor = get_object_or_404(UserProfile, user=request.user, is_professor=True)
        course = Course.objects.create(name=name, professor=professor)
        students = UserProfile.objects.filter(id__in=student_ids, is_student=True)
        course.students.set(students)
        
        return JsonResponse({"message": "Course created successfully!", "course_id": course.id})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def create_team(request):
    if request.method == "POST":
        name = request.POST.get("name")
        course_id = request.POST.get("course_id")
        member_ids = request.POST.getlist("members")
        course = get_object_or_404(Course, id=course_id, professor__user=request.user)
        team = Team.objects.create(name=name, course=course)
        members = UserProfile.objects.filter(id__in=member_ids, is_student=True, courses_enrolled=course)
        team.members.set(members)
        
        return JsonResponse({"message": "Team created successfully!", "team_id": team.id})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def dashboard_redirect(request):
    return redirect('/dashboard/')  # Change this if needed