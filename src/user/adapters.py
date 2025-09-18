from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse
from .models import StudentProfile, TeacherProfile
from .utils import get_dashboard_redirect

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        return get_dashboard_redirect(request.user)

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        if not user.username:
            email = user.email or ""
            base_name = email.split("@")[0] if "@" in email else "user"
            user.username = f"{base_name}{user.pk}"
            user.save(update_fields=["username"])

        return user
