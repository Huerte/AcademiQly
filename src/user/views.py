from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .utils import get_dashboard_redirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.cache import cache


def login_page(request):
    return render(request, 'auth/auth.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.has_usable_password():
                    messages.error(request, 'This account uses Google login. Please continue with Google.')
                elif user.check_password(password):
                    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                    redirect_url = get_dashboard_redirect(user)
                    messages.success(request, 'Login successful!')
                    return redirect(redirect_url)
                else:
                    messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return redirect('login_page')

def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not email or not password or not confirm_password:
            messages.error(request, 'Please fill in all fields.')
            return redirect('login_page')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('login_page')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('login_page')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('login_page')

        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(username=username, email=email, password=password)
        
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        messages.success(request, 'Registration successful!')
        return redirect('role_selection')
    
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
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        department = request.POST.get('department')
        years_of_exp = request.POST.get('years_of_exp')
        highest_qualification = request.POST.get('highest_qualification')
        specialization = request.POST.get('specialization', '')
        bio = request.POST.get('bio', '')
        phone_number = request.POST.get('phone_number', '')
        
        if first_name and last_name and department and years_of_exp and highest_qualification:

            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            TeacherProfile.objects.create(
                user=request.user,
                middle_name=middle_name,
                department=Course.objects.get(name=department),
                years_of_exp=years_of_exp,
                highest_qualification=Qualification.objects.get(name=highest_qualification),
                specialization=specialization,
                bio=bio,
                phone_number=phone_number
            )
            messages.success(request, 'Profile created successfully!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'qualifications': Qualification.objects.all(),
        'courses': Course.objects.all()
    }

    return render(request, 'section/setup/teacher_setup.html', context)

@login_required
def student_setup(request):
    if hasattr(request.user, 'student'):
        login(request.user)
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        course = request.POST.get('course')
        year_level = request.POST.get('year_level')
        academic_interest = request.POST.get('academic_interest', '')
        bio = request.POST.get('bio', '')
        phone_number = request.POST.get('phone_number', '')
        
        if first_name and last_name and student_id and course and year_level:
            if not hasattr(request.user, 'student'):

                user = request.user
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                StudentProfile.objects.create(
                    user=request.user,
                    middle_name=middle_name,
                    student_id=student_id,
                    course=Course.objects.get(name=course),
                    year_level=YearLevel.objects.get(name=year_level),
                    academic_interest=academic_interest,
                    bio=bio,
                    phone_number=phone_number
                )
                messages.success(request, 'Profile created successfully!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'courses': Course.objects.all(),
        'year_levels': YearLevel.objects.all()
    }

    return render(request, 'section/setup/student_setup.html', context)

@login_required
def view_profile(request, id):
    if request.user.is_authenticated:

        user = User.objects.get(id=id)

        if hasattr(user, 'teacher'):
            return render(request, 'section/profile/profile_teacher.html', {'profile': user.teacher})
        elif hasattr(user, 'student'):
            return render(request, 'section/profile/profile_student.html', {'profile': user.student})
        else:
            return redirect('role_selection')
        
    return redirect('login_page')

@login_required
def user_settings(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

    profile = None
    is_teacher = hasattr(request.user, 'teacher')
    is_student = hasattr(request.user, 'student')
    if is_teacher:
        profile = request.user.teacher
    elif is_student:
        profile = request.user.student

    if request.method == 'POST':
        section = request.POST.get('section')
        
        if section == 'account':
            email = request.POST.get('email', '').strip()
            first_name = request.POST.get('first_name', '').strip()
            middle_name = request.POST.get('middle_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            
            if email:
                request.user.email = email
            if first_name:
                request.user.first_name = first_name
            if middle_name:
                
                if hasattr(request.user, 'teacher'):
                    request.user.teacher.middle_name = middle_name
                    request.user.teacher.save()
                elif hasattr(request.user, 'student'):
                    request.user.student.middle_name = middle_name
                    request.user.student.save()
                    messages.success(request, f'Successfully added a middle name {middle_name}')

            if last_name:
                request.user.last_name = last_name
            request.user.save()
            
            messages.success(request, 'Account information updated successfully.')
            
        elif section == 'profile':
            if profile:
                phone_number = request.POST.get('phone_number', '').strip()
                profile_picture = request.FILES.get('profile_picture')
                bio = request.POST.get('bio', '').strip()
                profile.phone_number = phone_number
                profile.bio = bio

                if profile_picture:
                    profile.profile_picture = profile_picture

                profile.save()
                
                messages.success(request, 'Profile information updated successfully.')
                
        elif section == 'academic':
            if is_student and profile:
                student_id = request.POST.get('student_id', '').strip()
                course = request.POST.get('course', '').strip()
                year_level = request.POST.get('year_level', '').strip()
                academic_interest = request.POST.get('academic_interest', '').strip()
                
                if student_id:
                    profile.student_id = student_id
                if course:
                    profile.course = Course.objects.get(name=course)
                if year_level:
                    profile.year_level = YearLevel.objects.get(name=year_level)
                profile.academic_interest = academic_interest
                profile.save()
                
                messages.success(request, 'Academic information updated successfully.')
                
            elif is_teacher and profile:
                department = request.POST.get('department', '').strip()
                years_of_exp = request.POST.get('years_of_exp', '').strip()
                highest_qualification = request.POST.get('highest_qualification', '').strip()
                specialization = request.POST.get('specialization', '').strip()
                
                if department:
                    profile.department = Course.objects.get(id=department)
                if years_of_exp:
                    profile.years_of_exp = years_of_exp
                if highest_qualification:
                    profile.highest_qualification = Qualification.objects.get(id=highest_qualification)
                profile.specialization = specialization
                profile.save()
                
                messages.success(request, 'Academic information updated successfully.')
                
        elif section == 'password':
            current_password = request.POST.get('current_password', '').strip()
            new_password = request.POST.get('new_password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()
            
            if not new_password or not confirm_password:
                messages.error(request, 'Please fill in all password fields.')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            elif request.user.has_usable_password() and not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'Password updated successfully.')

        return redirect('user_settings')

    context = {
        'profile': profile,
        'is_teacher': is_teacher,
        'is_student': is_student,
        'year_levels': YearLevel.objects.all(),
        'courses': Course.objects.all(),
        'qualifications': Qualification.objects.all(),
    }
    return render(request, 'section/settings.html', context)

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password', '').strip()
        
        if password and request.user.check_password(password):
            if hasattr(request.user, 'teacher'):
                request.user.teacher.delete()
            elif hasattr(request.user, 'student'):
                request.user.student.delete()
            
            request.user.delete()
            
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('login_page')
        else:
            messages.error(request, 'Incorrect password. Account deletion failed.')
            return redirect('user_settings')
    
    return redirect('user_settings')

def send_password_reset_link(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        if email:
            if User.objects.filter(email=email).exists():

                reset_token = get_random_string(length=32)
                cache.set(reset_token, email, timeout=300) # Expires in 5 minutes

                try:
                    send_mail(
                        subject = 'Password Reset Request',
                        message = f"""
                        Click the link below to reset your password:
                        {settings.SITE_DOMAIN}/auth/reset-password/{reset_token}/

                        If you did not request a password reset, please ignore this email.""",
                        from_email = settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Password reset link sent to your email.')
                except Exception as e:
                    messages.error(request, 'Failed to send email.')
            else:
                messages.error(request, 'User with this email does not exist.')
    else:
        messages.error(request, 'Please provide a valid email address.')
        
    return redirect('login_page')

def reset_password(request, token):
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:

            email = cache.get(token)
            if not email:
                messages.error(request, 'Invalid or expired token.')
                return redirect('login_page')
            else:
                try:
                    user = User.objects.get(email=email)
                    user.set_password(new_password)
                    user.save()
                except User.DoesNotExist:
                    messages.error(request, 'User does not exist.')
                    return redirect('login_page')
                
                cache.delete(token)
                
                messages.success(request, 'Password has been reset successfully. Please log in with your new password.')
                return redirect('login_page')
    
    return render(request, 'auth/reset_password.html', {'token': token})
