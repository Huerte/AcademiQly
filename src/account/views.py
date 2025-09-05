from django.shortcuts import render, redirect


def login_page(request):
    return render(request, 'auth/login.html')

def register_page(request):
    return render(request, 'auth/register.html')

def profile_page(request):
    return render(request, 'section/profile.html')

def login_user(request):
    if request.method == 'POST':
        user_role = request.POST.get('role')

        if user_role:
            
            if user_role == 'teacher':
                return redirect('teacher_dashboard')
            elif user_role == 'student':
                return redirect('student_dashboard')

    return redirect('login_page')

def register_user(request):
    return redirect('login_page')