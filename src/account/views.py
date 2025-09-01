from django.shortcuts import render

def login_page(request):
    return render(request, 'auth/login.html')

def register_page(request):
    return render(request, 'auth/register.html')