from django.apps import AppConfig


class PeerconnectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PeerConnect'

    def ready(self):
        import PeerConnect.signals  # Ensure signals are imported