from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import StudentProfile, TeacherProfile

def get_dashboard_redirect(user):
    if user.is_superuser:
        return "/admin/"
    
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


def handle_unauthorized_access(request, message="You do not have permission to access this page."):
    messages.error(request, message)
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    else:
        return redirect('login_page')


def handle_not_found(request, message="The requested page was not found."):
    messages.warning(request, message)
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    else:
        return redirect('home')