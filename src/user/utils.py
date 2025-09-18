from django.urls import reverse
from .models import StudentProfile, TeacherProfile

def get_dashboard_redirect(user):
    try:
        if user.student:
            return reverse("user_dashboard")
    except StudentProfile.DoesNotExist:
        pass

    try:
        if user.teacher:
            return reverse("user_dashboard")
    except TeacherProfile.DoesNotExist:
        pass

    return reverse("role_selection")