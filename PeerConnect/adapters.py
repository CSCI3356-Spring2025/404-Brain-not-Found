from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        if sociallogin.user.is_authenticated:  # Check if user has already signed up
            return redirect('/student_dashboard/')  # Change to your actual dashboard URL
