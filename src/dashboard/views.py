from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from room.models import Room

def user_dashboard(request):

    if request.user.is_authenticated:
        user = request.user
        if hasattr(user, 'teacher'):
            my_rooms = Room.objects.filter(teacher=user)
            return render(request, 'section/teacher_dashboard.html', {'my_rooms': my_rooms, 'in_dashboard': True})
        elif hasattr(user, 'student'):
            return render(request, 'section/student_dashboard.html')
    
    return redirect('login')