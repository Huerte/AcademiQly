from django.shortcuts import render, redirect


def login_page(request):
    return render(request, 'auth/login.html')

def register_page(request):
    return render(request, 'auth/register.html')

def profile_teacher(request):
    return render(request, 'section/profile_teacher.html')

def profile_student(request):
    return render(request, 'section/profile_student.html')

def view_teacher_profile(request, teacher_id):
    return render(request, 'section/profile_teacher.html')

def view_student_profile(request, student_id):
    return render(request, 'section/profile_student.html')

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