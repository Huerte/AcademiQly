from django.shortcuts import render, redirect
from .models import Room, Activity, Announcement
from django.contrib.auth.models import User
from user.models import StudentProfile, TeacherProfile


def room_view(request, room_id):

    if request.user.is_authenticated:
        room = Room.objects.get(id=room_id)
        
        breadcrumb_items = [
            {'text': 'Dashboard', 'url': '/dashboard/', 'icon': 'bi bi-house'},
            {'text': 'My Rooms', 'url': '/room/all/', 'icon': 'bi bi-collection-play'},
            {'text': room.name, 'url': '', 'icon': 'bi bi-door-open'}
        ]
        
        context = {
            'room': room,
            'activities': Activity.objects.filter(room=room),
            'announcements': Announcement.objects.filter(room=room).order_by('-created_at'),
            'breadcrumb_items': breadcrumb_items
        }

        if hasattr(request.user, 'teacher'):
            return render(request, 'room.html', context)
        elif hasattr(request.user, 'student'):
            return render(request, 'room-student.html', context)
        
    return redirect('all_room')


def view_all_room(request):
    if request.user.is_authenticated:
        room = []
        if hasattr(request.user, 'teacher'):
            room = Room.objects.filter(teacher__user=request.user)
        elif hasattr(request.user, 'student'):
            room = Room.objects.filter(students=request.user)

        breadcrumb_items = [
            {'text': 'Dashboard', 'url': '/dashboard/', 'icon': 'bi bi-house'},
            {'text': 'My Rooms', 'url': '', 'icon': 'bi bi-collection-play'}
        ]

        context = {
            'rooms': room,
            'breadcrumb_items': breadcrumb_items
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

def activity_view(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    room = activity.room
    breadcrumb_items = [
        {'text': 'Dashboard', 'url': '/dashboard/', 'icon': 'bi bi-house'},
        {'text': 'My Rooms', 'url': '/room/all/', 'icon': 'bi bi-collection-play'},
        {'text': room.name, 'url': f'/room/{room.id}/', 'icon': 'bi bi-door-open'},
        {'text': 'Activity', 'url': '', 'icon': 'bi bi-journal-text'},
    ]
    
    context = {
        'breadcrumb_items': breadcrumb_items
    }
    return render(request, 'activity_teacher.html', context)

def activity_view_s(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    room = activity.room

    breadcrumb_items = [
        {'text': 'Dashboard', 'url': '/dashboard/', 'icon': 'bi bi-house'},
        {'text': 'My Rooms', 'url': '/room/all/', 'icon': 'bi bi-collection-play'},
        {'text': room.name, 'url': f'/room/{room.id}/', 'icon': 'bi bi-door-open'},
        {'text': 'Activity', 'url': '', 'icon': 'bi bi-journal-text'}
    ]
    
    context = {
        'breadcrumb_items': breadcrumb_items
    }
    return render(request, 'activity_student.html', context)

def announcement_view(request, announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)
    room = announcement.room
    breadcrumb_items = [
        {'text': 'Dashboard', 'url': '/dashboard/', 'icon': 'bi bi-house'},
        {'text': 'My Rooms', 'url': '/room/all/', 'icon': 'bi bi-collection-play'},
        {'text': room.name, 'url': f'/room/{room.id}/', 'icon': 'bi bi-door-open'},
        {'text': 'Announcement', 'url': '', 'icon': 'bi bi-megaphone'}
    ]
    
    context = {
        'announcement': announcement,
        'breadcrumb_items': breadcrumb_items
    }

    return render(request, 'announcement.html', context)


def create_room(request):
    if request.method == 'POST':
        
        if request.user.is_authenticated and hasattr(request.user, 'teacher'):
            name = request.POST.get('name')
            description = request.POST.get('description')
            teacher = TeacherProfile.objects.get(user=request.user)

            room = Room.objects.create(
                name=name,
                description=description,
                teacher=teacher
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