from django.urls import reverse
from .models import StudentProfile, TeacherProfile

def get_dashboard_redirect(user):
    try:
        if user.student:
            return reverse("student_dashboard")
    except StudentProfile.DoesNotExist:
        pass

    try:
        if user.teacher:
            return reverse("teacher_dashboard")
    except TeacherProfile.DoesNotExist:
        pass

    return reverse("role_selection")