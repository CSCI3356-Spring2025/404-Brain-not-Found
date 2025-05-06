from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from PeerConnect.models import Assessment, QuestionResponse, StudentProfile
from django.conf import settings
from datetime import timedelta


def remind_unsubmitted():
    print("Running reminder job")
    now = timezone.now()
    print("Now:", now)

        # gets date/time 12 hours from now
    twelve_hrs_later = now + timedelta(hours=24)
    print("Twelve hours later:", twelve_hrs_later)

        # filters due_dates <= 12 hrs away and >= now
        # ** Removed published=True because only want to remind for unpublished assessments
    upcoming_assessments = Assessment.objects.filter(due_date__lte=now + timezone.timedelta(hours=24), due_date__gte=now, published=False)

    print(f"Found {upcoming_assessments.count()} upcoming assessments.")
    #tomorrow = timezone.now().date() + timedelta(days=1)
    #assessments = Assessment.objects.filter(due_date__date=tomorrow, published=True)

    for assessment in upcoming_assessments:
        if not assessment.open_reminder_sent:

            for course in assessment.course.all():
                print(f"Course: {course.name}, students: {course.students.count()}")
                for student in course.students.all():
                    print(f"Checking student: {student.user.email}")
                    has_responded = QuestionResponse.objects.filter(
                        assessment=assessment,
                        student=student
                    ).exists()

                    print(f"Has responded: {has_responded}")

                    if not has_responded:
                        print("Sending email to", student.user.email)
                        user = student.user
                        send_mail(
                            subject=f"Reminder: Peer Assessment Due in 12 Hours",
                            message=(
                                f"Hi {user.first_name},\n\n"
                                f"You have not yet completed the peer assessment \"{assessment.name}\" "
                                f"for the course {course.name}.\n\n"
                                f"The deadline is {assessment.due_date.strftime('%Y-%m-%d %H:%M')}.\n"
                                f"Please log into PeerConnect and complete it before the deadline."
                            ),
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[user.email],
                            fail_silently=False,
                        )
            assessment.open_reminder_sent = True
            assessment.save()
        else:
            print("Assessment reminder already sent")