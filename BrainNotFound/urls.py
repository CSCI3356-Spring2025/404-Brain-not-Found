"""
URL configuration for BrainNotFound project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from PeerConnect import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('peer_answer_quant/', views.peer_answer_quant, name='peer_answer_quant'),
    path('peer_answer_qual/', views.peer_answer_qual, name='peer_answer_qual'),
    path('create/', views.create, name='create'),
    path('course_form/', views.course_form, name='course_form'),
    path('professor_dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('', views.landing_page, name="landing"),
    path('create_course/', views.create_course, name='create_course'),

    path('accounts/', include('allauth.urls')),

]
