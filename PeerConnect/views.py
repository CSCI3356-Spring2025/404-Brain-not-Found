from django.shortcuts import render

# Create your views here.
def student_dashboard(request):
    return render(request, "PeerConnect/student_dashboard.html", {})