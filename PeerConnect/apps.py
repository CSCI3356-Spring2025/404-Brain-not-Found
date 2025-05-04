from django.apps import AppConfig


class PeerconnectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PeerConnect'

    def ready(self):
        import PeerConnect.signals  # Ensure signals are imported

        #def ready(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        from PeerConnect.cron import remind_unsubmitted 

        scheduler = BackgroundScheduler()
        scheduler.add_job(remind_unsubmitted, 'interval', hours=1)  #run every hour?
        scheduler.start()


    