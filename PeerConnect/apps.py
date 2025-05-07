from django.apps import AppConfig
import os

class PeerconnectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PeerConnect'
    scheduler = None
    # def ready(self):
    #     import PeerConnect.signals  # Ensure signals are imported
    #     print("Creating scheduler")
    #     #def ready(self):
    #     from apscheduler.schedulers.background import BackgroundScheduler
    #     from PeerConnect.cron import remind_unsubmitted 

    #     scheduler = BackgroundScheduler()
        
    #     scheduler.add_job(remind_unsubmitted, 'interval', minutes=1)  #run every hour?
    #     print("Starting sched .")
    #     scheduler.start()
    #     print("Scheduler started")
    
    def ready(self):
        import PeerConnect.signals
        if os.environ.get('RUN_MAIN') == 'true':
            if not self.scheduler:
                import PeerConnect.signals  # Ensure signals are imported
                print("Creating scheduler")
                #def ready(self):
                from apscheduler.schedulers.background import BackgroundScheduler
                from PeerConnect.cron import remind_unsubmitted, remind_available

                self.scheduler = BackgroundScheduler()
                
                self.scheduler.add_job(remind_unsubmitted, 'interval', minutes=1)  #runs every 30mins
                print("Starting sched .")
                self.scheduler.start()
                print("Scheduler started")

                # Email for available (to edit) assessments
                self.scheduler.add_job(remind_available, 'interval', minutes=1)  #runs every 30mins
            else:
                print("Scheduler is already running")





    