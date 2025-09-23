from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from room.models import Room
from user.models import StudentProfile, TeacherProfile


def user_dashboard(request):

    if request.user.is_authenticated:
        user = request.user
        if hasattr(user, 'teacher'):
            teacher_profile = TeacherProfile.objects.get(user=user)
            my_rooms = Room.objects.filter(teacher=teacher_profile)
            total_students = sum(room.students.count() for room in my_rooms)
            total_activities = sum(room.activity_set.count() for room in my_rooms)
            total_announcements = sum(room.announcement_set.count() for room in my_rooms)
            
            context = {
                'my_rooms': my_rooms,
                'total_rooms': my_rooms.count(),
                'total_students': total_students,
                'total_activities': total_activities,
                'total_announcements': total_announcements,
                'in_dashboard': True
            }
            return render(request, 'teacher/dashboard.html', context)
        elif hasattr(user, 'student'):
            my_rooms = Room.objects.filter(students=user)
            return render(request, 'student/dashboard.html', {'course': my_rooms, 'in_dashboard': True})
    
    return redirect('login')