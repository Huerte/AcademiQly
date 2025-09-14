from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        return True

    def get_login_redirect_url(self, request):
        return reverse("role_selection")

    def get_connect_redirect_url(self, request, socialaccount):
        return reverse("role_selection")

    def get_signup_redirect_url(self, request, socialaccount):
        return reverse("role_selection")

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        return user