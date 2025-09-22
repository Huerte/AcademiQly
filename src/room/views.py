from django.shortcuts import render, redirect
from .models import Room, Activity, Announcement
from django.contrib.auth.models import User


def room_view(request, room_id):

    if request.user.is_authenticated:
        room = Room.objects.get(id=room_id)
        
        context = {
            'room': room,
            'activities': Activity.objects.filter(room=room),
            'announcements': Announcement.objects.filter(room=room).order_by('-created_at')
        }

        if hasattr(request.user, 'teacher'):
            return render(request, 'room.html', context)
        elif hasattr(request.user, 'student'):
            return render(request, 'room-student.html', context)
        
    return redirect('all_room')


def view_all_room(request):
    if request.user.is_authenticated:

        room = Room.objects.all()

        context = {
            'rooms': room
        }

        return render(request, 'rooms.html', context)

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

def create_activity(request):
    if request.method == 'POST':

        if request.user.is_authenticated and hasattr(request.user, 'teacher'):
            title = request.POST.get('title')
            description = request.POST.get('description')
            due_date = request.POST.get('deadline')
            room_id = request.POST.get('room_id')
            total_marks = request.POST.get('total_points')

            room = Room.objects.get(id=room_id)

            activity = Activity.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                room=room,
                total_marks=total_marks
            )
            activity.save()
            return redirect('room', room_id=room.id)

    return redirect('all_room')


def create_announcement(request):
    if request.method == 'POST':

        if request.user.is_authenticated and hasattr(request.user, 'teacher'):
            title = request.POST.get('title')
            content = request.POST.get('content')
            room_id = request.POST.get('room_id')

            room = Room.objects.get(id=room_id)

            announcement = Announcement.objects.create(
                title=title,
                content=content,
                room=room
            )
            announcement.save()
            return redirect('room', room_id=room.id)

    return redirect('all_room')