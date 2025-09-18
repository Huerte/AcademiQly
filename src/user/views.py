from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentProfile, TeacherProfile
from .utils import get_dashboard_redirect
from django.urls import reverse
from django.contrib.auth import login, logout


def login_page(request):
    return render(request, 'auth/login.html')

def logout_user(request):
    logout(request.user)
    return redirect('login_page')

@login_required
def role_selection(request):
    
    if request.user.is_authenticated:
        redirect_url = get_dashboard_redirect(request.user)
        if redirect_url != reverse('role_selection'):
            return redirect(redirect_url)

    return render(request, 'auth/role_selection.html')

@login_required
def select_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        
        if role == 'student':
            return redirect('student_setup')
        elif role == 'teacher':
            return redirect('teacher_setup')
        else:
            messages.error(request, 'Please select a valid role.')
            return redirect('role_selection')
    
    return redirect('role_selection')

@login_required
def teacher_setup(request):
    if hasattr(request.user, 'teacher'):
        login(request.user)
        return redirect('teacher_dashboard')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        department = request.POST.get('department')
        years_of_exp = request.POST.get('years_of_exp')
        highest_qualification = request.POST.get('highest_qualification')
        specialization = request.POST.get('specialization', '')
        bio = request.POST.get('bio', '')
        phone_number = request.POST.get('phone_number', '')
        
        if full_name and department and years_of_exp and highest_qualification:
            TeacherProfile.objects.create(
                user=request.user,
                full_name=full_name,
                department=department,
                years_of_exp=years_of_exp,
                highest_qualification=highest_qualification,
                specialization=specialization,
                bio=bio,
                phone_number=phone_number
            )
            messages.success(request, 'Profile created successfully!')
            return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'section/setup/teacher_setup.html')

@login_required
def student_setup(request):
    if hasattr(request.user, 'student'):
        login(request.user)
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        student_id = request.POST.get('student_id')
        course = request.POST.get('course')
        year_level = request.POST.get('year_level')
        section = request.POST.get('section')
        academic_interest = request.POST.get('academic_interest', '')
        bio = request.POST.get('bio', '')
        phone_number = request.POST.get('phone_number', '')
        
        if full_name and student_id and course and year_level and section:
            if not hasattr(request.user, 'student'):
                StudentProfile.objects.create(
                    user=request.user,
                    full_name=full_name,
                    student_id=student_id,
                    course=course,
                    year_level=year_level,
                    section=section,
                    academic_interest=academic_interest,
                    bio=bio,
                    phone_number=phone_number
                )
                messages.success(request, 'Profile created successfully!')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'section/setup/student_setup.html')

def view_teacher_profile(request):
    return render(request, 'section/profile/profile_teacher.html')

def view_student_profile(request):
    return render(request, 'section/profile/profile_student.html')

