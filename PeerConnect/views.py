from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Course, Team

# Create your views here.
def student_dashboard(request):
    #user_profile = get_object_or_404(UserProfile, user=request.user)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if not user_profile.is_professor:
        user_type = "Student"
    else:
        user_type = "Professor"
    return render(request, "PeerConnect/student_dashboard.html", {'user': request.user, 'type': user_type})

def peer_answer_qual(request):
    return render(request, "PeerConnect/peer_answer_qual.html", {})

def peer_answer_quant(request):
    return render(request, "PeerConnect/peer_answer_quant.html", {})

def create(request):
    return render(request, "PeerConnect/create.html", {})

def landing_page(request):
    return render(request, "PeerConnect/landingpage.html", {})


def signup_view(request):
    # Check if user is already signed up
    if request.user.is_authenticated:
        return redirect('/student_dashboard/')  # Change this to your actual dashboard URL
    return render(request, "signup.html")

@login_required
def dashboard_redirect(request):
    return redirect('/dashboard/')  # Change this if needed