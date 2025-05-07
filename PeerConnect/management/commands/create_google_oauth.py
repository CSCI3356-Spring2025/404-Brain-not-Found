from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
import os

class Command(BaseCommand):
    help = "Creates the Google OAuth app for django-allauth if not present."

    def handle(self, *args, **kwargs):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        secret = os.getenv("GOOGLE_SECRET")

        if not client_id or not secret:
            self.stderr.write("Missing GOOGLE_CLIENT_ID or GOOGLE_SECRET env vars.")
            return

        site = Site.objects.get_current()
        if not SocialApp.objects.filter(provider="google").exists():
            app = SocialApp.objects.create(
                provider="google",
                name="Google",
                client_id=client_id,
                secret=secret,
            )
            app.sites.add(site)
            self.stdout.write("✅ Google OAuth app created.")
        else:
            self.stdout.write("✅ Google OAuth app already exists.")