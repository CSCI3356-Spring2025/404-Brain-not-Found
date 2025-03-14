from django.shortcuts import render

# Create your views here.
def student_dashboard(request):
    return render(request, "PeerConnect/student_dashboard.html", {})

def peer_answer_qual(request):
    return render(request, "PeerConnect/peer_answer_qual.html", {})

def peer_answer_quant(request):
    return render(request, "PeerConnect/peer_answer_quant.html", {})

def landing_page(request):
    return render(request, "PeerConnect/landingpage.html", {})