from django.shortcuts import render, redirect


def login_page(request):
    return render(request, 'auth/login.html')

def register_page(request):
    return render(request, 'auth/register.html')

def profile_page(request):
    return render(request, 'section/profile.html')

def login_user(request):
    return redirect('student_dashboard')

def register_user(request):
    return redirect('student_dashboard')