from django.shortcuts import redirect
from django.contrib.auth.models import AnonymousUser

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            user = getattr(request, 'user', AnonymousUser())
            
            if not user.is_authenticated:
                return redirect('login_page')
            
            if not user.is_superuser:
                return redirect('user_dashboard')

        response = self.get_response(request)
        return response
