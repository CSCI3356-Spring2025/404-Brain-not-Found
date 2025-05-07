from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from .models import UserProfile

""" @receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance) """

@receiver(user_logged_in)
def assign_role_on_login(sender, request, user, **kwargs):
    if user.email == "shahpj@bc.edu":
        # Mark this user as a professor
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.is_professor = True
        user_profile.save()
    else:
        # Mark other users as students
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.is_professor = False
        user_profile.save()

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.userprofile.save()