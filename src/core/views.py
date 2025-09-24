from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext


def homepage(request):
    return render(request, 'home.html')


def custom_404(request, exception=None):
    context = {
        'error_code': '404',
        'error_title': 'Page Not Found',
        'error_message': 'The page you are looking for does not exist.',
        'error_description': 'The requested page could not be found. It may have been moved, deleted, or you may have entered an incorrect URL.',
    }
    return render(request, 'errors/error.html', context, status=404)


def custom_500(request):
    context = {
        'error_code': '500',
        'error_title': 'Server Error',
        'error_message': 'Something went wrong on our end.',
        'error_description': 'We are experiencing technical difficulties. Please try again later or contact support if the problem persists.',
    }
    return render(request, 'errors/error.html', context, status=500)


def custom_403(request, exception=None):
    context = {
        'error_code': '403',
        'error_title': 'Access Forbidden',
        'error_message': 'You do not have permission to access this page.',
        'error_description': 'You are not authorized to view this content. Please contact an administrator if you believe this is an error.',
    }
    return render(request, 'errors/error.html', context, status=403)


def custom_400(request, exception=None):
    context = {
        'error_code': '400',
        'error_title': 'Bad Request',
        'error_message': 'Your request could not be processed.',
        'error_description': 'The server could not understand your request. Please check your input and try again.',
    }
    return render(request, 'errors/error.html', context, status=400)


def test_404(request):
    from django.http import Http404
    raise Http404("This is a test 404 error")


def test_500(request):
    raise Exception("This is a test 500 error")


def test_403(request):
    from django.core.exceptions import PermissionDenied
    raise PermissionDenied("This is a test 403 error")