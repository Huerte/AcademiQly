from django.shortcuts import render, redirect
from .models import Room, Activity, Announcement
from django.contrib.auth.models import User


def room_view(request, room_id):

    if request.user.is_authenticated:
        room = Room.objects.get(id=room_id)

        context = {
            'room': room
        }

        if hasattr(request.user, 'teacher'):
            return render(request, 'room.html', context)
        elif hasattr(request.user, 'student'):
            return render(request, 'room-student.html', context)
        
    return redirect('all_room')


def view_all_room(request):
    if request.user.is_authenticated:
        return render(request, 'rooms.html')

    return redirect('home')

def enroll_student(request):
    if request.method == 'POST':
        room_code = request.POST.get('code')
        room = Room.objects.filter(room_code=room_code).exists()
        if room:
            room = Room.objects.get(room_code=room_code)
            room.students.add(request.user)
            room.save()
            return redirect('room', room_id=room.id)
            
    return redirect('all_room')

def activity_view(request):
    return render(request, 'activity_teacher.html')

def activity_view_s(request):
    return render(request, 'activity_student.html')

def announcement_view(request):
    return render(request, 'announcement.html')


def create_room(request):
    if request.method == 'POST':
        
        if request.user.is_authenticated and hasattr(request.user, 'teacher'):
            name = request.POST.get('name')
            description = request.POST.get('description')

            room = Room.objects.create(
                name=name,
                description=description,
                teacher=request.user
            )
            room.save()
            return redirect('room', room_id=room.id)

    return redirect('all_room')