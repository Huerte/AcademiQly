from django.shortcuts import render, redirect


def login_page(request):
    return render(request, 'auth/login.html')

def register_page(request):
    return render(request, 'auth/register.html')

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
    if request.method == 'POST':
        user_role = request.POST.get('role')
        
        if user_role == 'teacher':
            return redirect('teacher_setup')
        elif user_role == 'student':
            return redirect('student_setup')
    
    return redirect('register_page')

def teacher_setup(request):
    return render(request, 'section/setup/teacher_setup.html')

def student_setup(request):
    return render(request, 'section/setup/student_setup.html')

def view_teacher_profile(request):
    return render(request, 'section/profile/profile_teacher.html')

def view_student_profile(request):
    return render(request, 'section/profile/profile_student.html')