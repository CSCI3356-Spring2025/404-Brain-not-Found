from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from PeerConnect.models import Assessment, QuestionResponse, StudentProfile
from django.conf import settings
from datetime import timedelta


def remind_unsubmitted():
    tomorrow = timezone.now().date() + timedelta(days=1)
    assessments = Assessment.objects.filter(due_date__date=tomorrow, published=True)

    for assessment in assessments:
        for course in assessment.course.all():
            for student in course.students.all():
                has_responded = QuestionResponse.objects.filter(
                    assessment=assessment,
                    student=student
                ).exists()

                if not has_responded:
                    user = student.user
                    send_mail(
                        subject=f"Reminder: Peer Assessment Due Tomorrow",
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