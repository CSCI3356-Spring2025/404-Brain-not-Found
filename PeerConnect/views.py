from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def student_dashboard(request):
    return render(request, "PeerConnect/student_dashboard.html", {})

def peer_answer_qual(request):
    return render(request, "PeerConnect/peer_answer_qual.html", {})

def peer_answer_quant(request):
    return render(request, "PeerConnect/peer_answer_quant.html", {})

def course_team_creation(request):
    return render(request, "PeerConnect/course_team_creation.html", {})

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