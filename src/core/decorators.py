from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404
from django.core.exceptions import PermissionDenied


def handle_errors(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Http404:
            messages.warning(request, 'The requested page was not found.')
            if request.user.is_authenticated:
                return redirect('user_dashboard')
            else:
                return redirect('home')
        except PermissionDenied:
            messages.error(request, 'You do not have permission to access this page.')
            if request.user.is_authenticated:
                return redirect('user_dashboard')
            else:
                return redirect('login_page')
        except Exception as e:
            messages.error(request, 'An unexpected error occurred. Please try again.')
            if request.user.is_authenticated:
                return redirect('user_dashboard')
            else:
                return redirect('home')
    return wrapper


def require_authentication(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login_page')
        return view_func(request, *args, **kwargs)
    return wrapper


def require_profile(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login_page')
        
        if not (hasattr(request.user, 'student') or hasattr(request.user, 'teacher')):
            messages.warning(request, 'Please complete your profile setup.')
            return redirect('role_selection')
        
        return view_func(request, *args, **kwargs)
    return wrapper
