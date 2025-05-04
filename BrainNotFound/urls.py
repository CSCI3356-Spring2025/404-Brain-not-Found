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
    path('course_roster/<int:course_id>/', views.course_roster, name='course_roster'),


    path('course_form/', views.course_form, name='course_form'),
    path('professor_dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('', views.landing_page, name="landing"),
    path('create_course/', views.create_course, name='create_course'),
    path('edit_course/<int:course_id>', views.edit_course, name='edit_course'),
    path('assessment/<int:course_id>/<int:assessment_id>/', views.delete_assessment, name='delete_assessment'),
    path('create_team/<int:course_id>', views.render_create_team, name='render_create_team'),
    path('save_team/<int:course_id>/', views.create_team, name='save_team'), 
    path('create_assessment', views.create_assessment, name='create_assessment'),
    path('view_assessment/<int:assessment_id>/', views.view_assessment, name='view_assessment'),

    path('delete_course/<int:course_id>', views.delete_course, name='delete_course'),
    path('delete_team/<int:team_id>', views.delete_team, name='delete_team'), 
    path('submit_assessment/<int:assessment_id>', views.submit_assessment, name='submit_assessment'),
    path('assessment_summary/<int:assessment_id>', views.assessment_summary, name='assessment_summary'),
    path('publish_assessment/<int:assessment_id>', views.publish_assessment, name='publish_assessment'),
    path('student_results/<int:assessment_id>', views.student_results, name='student_results'),
    path('past_due_date/', views.past_due_date, name='past_due_date'),

    path('accept_invitation/<uuid:token>/', views.accept_invitation, name='accept_invitation'),
    path("courses/<int:course_id>/roster/", views.course_roster, name="course_roster"),


    path('accounts/', include('allauth.urls')),

]
