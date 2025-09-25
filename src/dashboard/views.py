from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.utils.timesince import timesince
from room.models import Room, Activity, Submission
from user.models import StudentProfile, TeacherProfile
from django.contrib.auth.decorators import login_required


@login_required
def build_teacher_dashboard(request, user):
    Activity.close_past_due_bulk()
    teacher_profile = user.teacher
    my_rooms = Room.objects.filter(teacher=teacher_profile)
    room_ids = list(my_rooms.values_list('id', flat=True))

    total_students = sum(r.students.count() for r in my_rooms)
    total_activities = Activity.objects.filter(room_id__in=room_ids).count()
    total_announcements = sum(r.announcement_set.count() for r in my_rooms)

    activities = Activity.objects.filter(room_id__in=room_ids)
    grading_queue = [
        {"activity": a, "pending_count": Submission.objects.filter(activity=a, score__isnull=True).count()}
        for a in activities
        if Submission.objects.filter(activity=a, score__isnull=True).exists()
    ]

    q = request.GET.get('q', '').strip()
    course_filter = request.GET.get('course', '').strip()

    students_qs = User.objects.filter(students__in=my_rooms).distinct()
    if q:
        students_qs = students_qs.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q) |
            Q(username__icontains=q)
        )
    if course_filter:
        students_qs = students_qs.filter(students__name=course_filter)

    students_list = []
    for stu in students_qs:
        rooms_for_student = my_rooms.filter(students=stu)
        students_list.append({
            "initials": f"{stu.first_name[:1]}{stu.last_name[:1]}".upper() or stu.username[:2].upper(),
            "name": stu.get_full_name() or stu.username,
            "email": stu.email,
            "courses": ", ".join(r.name for r in rooms_for_student),
            "last_active": stu.last_login,
        })

    pending_qs = Submission.objects.filter(activity__room_id__in=room_ids, score__isnull=True)
    graded_qs = Submission.objects.filter(activity__room_id__in=room_ids, score__isnull=False)
    grading_stats = {"pending": pending_qs.count(), "in_review": 0, "graded": graded_qs.count()}

    pending_submissions = []
    for s in pending_qs.select_related('student__user', 'activity__room')[:50]:
        priority, color = "Medium", "warning"
        if s.activity.due_date:
            delta_days = (s.activity.due_date - timezone.now()).days
            if s.activity.due_date < timezone.now():
                priority, color = "High", "danger"
            elif delta_days <= 1:
                priority, color = "High", "danger"
            elif delta_days <= 3:
                priority, color = "Medium", "warning"
            else:
                priority, color = "Low", "success"

        pending_submissions.append({
            "student_name": s.student.user.get_full_name() or s.student.user.username,
            "assignment_name": s.activity.title,
            "course_code": s.activity.room.room_code,
            "submitted_time": timesince(s.submitted_at) + " ago",
            "priority": priority,
            "priority_color": color,
        })

    room_q = request.GET.get('room_q', '').strip()
    filtered_rooms = my_rooms.filter(Q(name__icontains=room_q) | Q(room_code__icontains=room_q)) if room_q else my_rooms

    return {
        "my_rooms": my_rooms,
        "filtered_rooms": filtered_rooms,
        "total_rooms": my_rooms.count(),
        "total_students": total_students,
        "total_activities": total_activities,
        "total_announcements": total_announcements,
        "grading_queue": grading_queue,
        "students": students_list,
        "courses_filter_options": list(my_rooms.values_list('name', flat=True)),
        "selected_q": q,
        "selected_course": course_filter,
        "grading_stats": grading_stats,
        "pending_submissions": pending_submissions,
        "in_dashboard": True,
        "room_q": room_q,
    }

@login_required
def build_student_dashboard(request, user):
    Activity.close_past_due_bulk()
    student_profile = user.student
    my_rooms = Room.objects.filter(students=user)

    room_q = (request.GET.get('room_q') or '').strip()
    a_q = (request.GET.get('a_q') or '').strip()
    a_status = (request.GET.get('a_status') or '').strip().lower()  
    a_course = (request.GET.get('a_course') or '').strip()  

    my_courses = [{
        "id": room.id,
        "name": room.name,
        "code": room.room_code,
        "instructor": room.teacher.full_name,
        "status": "Active"
    } for room in my_rooms]

    filtered_my_courses = my_courses
    if room_q:
        rq = room_q.lower()
        filtered_my_courses = [c for c in my_courses if rq in c["name"].lower() or rq in c["code"].lower()]

    all_activities = Activity.objects.filter(room__in=my_rooms).order_by('due_date')
    subs_by_activity = {s.activity_id: s for s in Submission.objects.filter(activity__in=all_activities, student=student_profile)}

    assignments, pending, overdue, submitted = [], 0, 0, 0
    for a in all_activities:
        sub = subs_by_activity.get(a.id)
        status, status_class, grade_display = "Pending", "pending", "—"

        if sub:
            if sub.score is not None:
                status, status_class, grade_display = "Graded", "graded", f"{sub.score} / {a.total_marks}"
                submitted += 1
            else:
                status, status_class, grade_display = "Submitted", "submitted", "Pending"
                submitted += 1
        else:
            if a.due_date and a.due_date < timezone.now():
                status, status_class, overdue = "Overdue", "overdue", overdue + 1
            else:
                pending += 1

        assignments.append({
            "name": a.title,
            "course_code": a.room.room_code,
            "course_name": a.room.name,
            "due_date": a.due_date,
            "status": status,
            "status_class": status_class,
            "grade": grade_display,
            "activity_id": a.id
        })

    filtered_assignments = assignments
    if a_q:
        ql = a_q.lower()
        filtered_assignments = [x for x in filtered_assignments if ql in x["name"].lower() or ql in x["course_name"].lower() or ql in x["course_code"].lower()]
    if a_status in {"pending", "submitted", "graded"}:
        filtered_assignments = [x for x in filtered_assignments if x["status_class"] == a_status]
    if a_course:
        filtered_assignments = [x for x in filtered_assignments if x["course_name"] == a_course]

    course_options = list(my_rooms.values_list('name', flat=True))

    return {
        "in_dashboard": True,
        "my_courses": my_courses,
        "filtered_my_courses": filtered_my_courses,
        "total_courses": len(my_courses),
        "room_q": room_q,
        "pending_assignments": pending,
        "assignments": filtered_assignments,
        "assignment_stats": {"pending": pending, "submitted": submitted, "overdue": overdue, "total": len(assignments)},
        "a_q": a_q,
        "a_status": a_status,
        "a_course": a_course,
        "assignment_course_options": course_options,
        "upcoming_activities": [a for a in all_activities if a.due_date and a.due_date >= timezone.now()][:5],
    }

@login_required
def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if hasattr(request.user, "teacher"):
        context = build_teacher_dashboard(request, request.user)
        return render(request, "teacher/dashboard.html", context)

    if hasattr(request.user, "student"):
        context = build_student_dashboard(request, request.user)
        return render(request, "student/dashboard.html", context)

    return redirect("login")
