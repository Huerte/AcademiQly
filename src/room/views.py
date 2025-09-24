from django.shortcuts import render, redirect
from .models import Room, Activity, Announcement, Submission
from django.contrib.auth.models import User
from user.models import StudentProfile, TeacherProfile
from utils.supabase_upload import upload_file


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
            'activities': Activity.objects.filter(room=room).order_by('-created_at'),
            'announcements': Announcement.objects.filter(room=room).order_by('-created_at'),
            'breadcrumb_items': breadcrumb_items
        }

        if hasattr(request.user, 'teacher'):
            return render(request, 'room/teacher.html', context)
        elif hasattr(request.user, 'student'):
            try:
                student_profile = StudentProfile.objects.get(user=request.user)
            except StudentProfile.DoesNotExist:
                student_profile = None

            activities = context['activities']
            submissions = []
            if student_profile:
                submissions = list(Submission.objects.filter(activity__in=activities, student=student_profile))
            submissions_by_activity = {s.activity_id: s for s in submissions}

            pending_count = 0
            scored_sum = 0
            possible_sum = 0
            for activity in activities:
                submission = submissions_by_activity.get(activity.id)
                if submission is None or submission.score is None:
                    pending_count += 1
                if submission is not None and submission.score is not None:
                    scored_sum += int(submission.score)
                    possible_sum += int(activity.total_marks or 0)

            overall_percent = 0
            if possible_sum > 0:
                overall_percent = round((scored_sum / possible_sum) * 100)

            context.update({
                'student_pending_activities': pending_count,
                'student_overall_percent': overall_percent,
            })

            return render(request, 'room/student.html', context)
        
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
        'breadcrumb_items': breadcrumb_items,
        'submission': None,
        'activity': activity,
    }

    if hasattr(request.user, 'student'):
        try:
            student = StudentProfile.objects.get(user=request.user)
            submission = Submission.objects.get(activity=activity, student=student)
            context['submission'] = submission
        except Submission.DoesNotExist:
            context['submission'] = None
        return render(request, 'activity/student.html', context)
    elif hasattr(request.user, 'teacher'):
        submissions = Submission.objects.filter(activity=activity)
        context['submissions'] = submissions
        return render(request, 'activity/teacher.html', context)
    return redirect('all_room')

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

def delete_room(request, room_id):
    if request.user.is_authenticated and hasattr(request.user, 'teacher'):
        room = Room.objects.get(id=room_id)
        if room.teacher.user == request.user:
            room.delete()
    return redirect('all_room')

def create_activity(request):
    if request.method == 'POST' and request.user.is_authenticated and hasattr(request.user, 'teacher'):
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('deadline')
        room_id = request.POST.get('room_id')
        total_marks = request.POST.get('total_points')
        resource_file = request.FILES.get('resource')

        room = Room.objects.get(id=room_id)

        activity = Activity.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            room=room,
            total_marks=total_marks
        )

        if resource_file:
            file_name = f"activities/{room.id}/{resource_file.name}"
            public_url = upload_file("activity-resources", resource_file, file_name)
            activity.resource_url = public_url
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

def submit_activity(request):
    if request.method == 'POST':
        if request.user.is_authenticated and hasattr(request.user, 'student'):
            activity_id = request.POST.get('activity_id')
            submission_file = request.FILES.get('submission_file')

            if activity_id and submission_file:
                activity = Activity.objects.get(id=activity_id)
                student = StudentProfile.objects.get(user=request.user)

                file_name = f"submissions/{activity.id}/{request.user.id}_{submission_file.name}"
                public_url = upload_file("submissions", submission_file, file_name)

                submission, created = Submission.objects.get_or_create(
                    activity=activity,
                    student=student,
                    defaults={'file_url': public_url}
                )

                if not created:
                    submission.file_url = public_url
                    submission.save()

                activity.status = 'submitted'
                activity.save()
                
                return redirect('activity_view', activity_id=activity_id)

    return redirect('all_room')

def grade_submission(request):
    if request.method == 'POST':
        if request.user.is_authenticated and hasattr(request.user, 'teacher'):
            submission_id = request.POST.get('submission_id')
            score = request.POST.get('score')
            feedback = request.POST.get('feedback')

            submission = Submission.objects.get(id=submission_id)
            activity = submission.activity
            room = activity.room

            if room.teacher.user == request.user:
                submission.score = score
                submission.feedback = feedback
                submission.save()

                submission.activity.status = 'graded'
                submission.activity.save()

                return redirect('activity_view', activity_id=activity.id)

    return redirect('all_room')

