from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from room.models import Room, Activity, Submission
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

            # Build grading queue: activities with pending submissions (no score yet)
            room_ids = list(my_rooms.values_list('id', flat=True))
            activities = Activity.objects.filter(room_id__in=room_ids)
            grading_queue = []
            for activity in activities:
                pending_count = Submission.objects.filter(activity=activity, score__isnull=True).count()
                if pending_count > 0:
                    grading_queue.append({
                        'activity': activity,
                        'pending_count': pending_count,
                    })

            # Filters for students section
            q = request.GET.get('q', '').strip()
            course_filter = request.GET.get('course', '').strip()
            grade_filter = request.GET.get('grade', '').strip().upper()

            students_qs = User.objects.filter(students__in=my_rooms).distinct()
            if q:
                students_qs = students_qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q) | Q(username__icontains=q))
            if course_filter:
                students_qs = students_qs.filter(students__room_code=course_filter)

            # Helper to compute grade from submissions
            def compute_student_grade(student_user: User) -> tuple[str, str]:
                profile = StudentProfile.objects.filter(user=student_user).first()
                if not profile:
                    return ("—", "c")
                subs = Submission.objects.filter(activity__room_id__in=room_ids, student=profile)
                scored = 0
                possible = 0
                for s in subs:
                    if s.score is not None and s.activity.total_marks:
                        scored += int(s.score)
                        possible += int(s.activity.total_marks)
                if possible == 0:
                    return ("—", "c")
                pct = (scored / possible) * 100
                if pct >= 90:
                    return ("A", "a")
                if pct >= 80:
                    return ("B", "b")
                if pct >= 70:
                    return ("C", "c")
                if pct >= 60:
                    return ("D", "d")
                return ("F", "f")

            students_list = []
            for stu in students_qs:
                rooms_for_student = my_rooms.filter(students=stu)
                courses_str = ", ".join(r.name for r in rooms_for_student)
                grade_letter, grade_class = compute_student_grade(stu)
                students_list.append({
                    'initials': f"{stu.first_name[:1]}{stu.last_name[:1]}".upper() or stu.username[:2].upper(),
                    'name': stu.get_full_name() or stu.username,
                    'email': stu.email,
                    'courses': courses_str,
                    'grade': grade_letter,
                    'grade_class': grade_class,
                    'last_active': getattr(stu, 'last_login', None),
                })

            if grade_filter in {"A", "B", "C", "D", "F"}:
                grade_map = {"A": "a", "B": "b", "C": "c", "D": "d", "F": "f"}
                students_list = [s for s in students_list if s['grade_class'] == grade_map[grade_filter]]

            courses_filter_options = list(my_rooms.values_list('room_code', flat=True))

            pending_qs = Submission.objects.filter(activity__room_id__in=room_ids, score__isnull=True)
            graded_qs = Submission.objects.filter(activity__room_id__in=room_ids, score__isnull=False)
            grading_stats = {
                'pending': pending_qs.count(),
                'in_review': 0,
                'graded': graded_qs.count(),
            }

            from django.utils.timesince import timesince
            pending_submissions = []
            for s in pending_qs.select_related('student__user', 'activity__room')[:50]:
                priority = 'Medium'
                priority_color = 'warning'
                if s.activity.due_date:
                    from django.utils import timezone
                    if s.activity.due_date < timezone.now():
                        priority, priority_color = 'High', 'danger'
                    elif (s.activity.due_date - timezone.now()).days <= 1:
                        priority, priority_color = 'High', 'danger'
                    elif (s.activity.due_date - timezone.now()).days <= 3:
                        priority, priority_color = 'Medium', 'warning'
                    else:
                        priority, priority_color = 'Low', 'success'

                pending_submissions.append({
                    'student_name': s.student.user.get_full_name() or s.student.user.username,
                    'assignment_name': s.activity.title,
                    'course_code': s.activity.room.room_code,
                    'submitted_time': timesince(s.submitted_at) + ' ago',
                    'priority': priority,
                    'priority_color': priority_color,
                })

            # Rooms filtering
            room_q = request.GET.get('room_q', '').strip()
            if room_q:
                filtered_rooms = my_rooms.filter(Q(name__icontains=room_q) | Q(room_code__icontains=room_q))
            else:
                filtered_rooms = my_rooms

            context = {
                'my_rooms': my_rooms,
                'filtered_rooms': filtered_rooms,
                'total_rooms': my_rooms.count(),
                'total_students': total_students,
                'total_activities': total_activities,
                'total_announcements': total_announcements,
                'grading_queue': grading_queue,
                'students': students_list,
                'courses_filter_options': courses_filter_options,
                'selected_q': q,
                'selected_course': course_filter,
                'selected_grade': grade_filter,
                'grading_stats': grading_stats,
                'pending_submissions': pending_submissions,
                'in_dashboard': True,
                'room_q': room_q,
            }
            return render(request, 'teacher/dashboard.html', context)
        elif hasattr(user, 'student'):
            student_profile = StudentProfile.objects.get(user=user)
            my_rooms = Room.objects.filter(students=user)

            my_courses = []
            for room in my_rooms:
                activities = Activity.objects.filter(room=room)
                subs = Submission.objects.filter(activity__in=activities, student=student_profile)
                scored_sum = sum(int(s.score) for s in subs if s.score is not None)
                possible_sum = sum(int(a.total_marks or 0) for a in activities if any(sub.activity_id == a.id and sub.score is not None for sub in subs))
                progress_percent = 0
                if possible_sum > 0:
                    progress_percent = round((scored_sum / possible_sum) * 100)
                my_courses.append({
                    'id': room.id,
                    'name': room.name,
                    'code': room.room_code,
                    'instructor': room.teacher.full_name,
                    'status': 'Active',
                    'progress': progress_percent,
                })

            total_courses = len(my_courses)

            all_activities = Activity.objects.filter(room__in=my_rooms).order_by('due_date')
            user_submissions = Submission.objects.filter(activity__in=all_activities, student=student_profile)
            subs_by_activity = {s.activity_id: s for s in user_submissions}

            assignments = []
            pending_count = 0
            overdue_count = 0
            submitted_count = 0
            for activity in all_activities:
                submission = subs_by_activity.get(activity.id)
                status = 'Pending'
                status_class = 'pending'
                grade_display = '—'
                if submission and submission.score is not None:
                    status = 'Submitted'
                    status_class = 'submitted'
                    grade_display = f"{submission.score} / {activity.total_marks}"
                    submitted_count += 1
                else:
                    if activity.due_date and activity.due_date < __import__('django.utils.timezone').utils.timezone.now():
                        status = 'Overdue'
                        status_class = 'overdue'
                        overdue_count += 1
                    else:
                        pending_count += 1

                assignments.append({
                    'name': activity.title,
                    'course_code': activity.room.room_code,
                    'due_date': activity.due_date,
                    'status': status,
                    'status_class': status_class,
                    'grade': grade_display,
                    'activity_id': activity.id,
                })

            assignment_stats = {
                'pending': pending_count,
                'submitted': submitted_count,
                'overdue': overdue_count,
                'total': len(assignments),
            }

            from django.utils import timezone
            now = timezone.now()
            upcoming_activities = [a for a in all_activities if a.due_date and a.due_date >= now][:5]

            graded_scored = 0
            graded_possible = 0
            for s in user_submissions:
                if s.score is not None and s.activity.total_marks:
                    graded_scored += int(s.score)
                    graded_possible += int(s.activity.total_marks)
            overall_percent = (graded_scored / graded_possible) * 100 if graded_possible > 0 else 0
            current_gpa = round((overall_percent / 100) * 4, 2)

            context = {
                'in_dashboard': True,
                'my_courses': my_courses,
                'total_courses': total_courses,
                'pending_assignments': pending_count,
                'current_gpa': f"{current_gpa:.2f}",
                'assignments': assignments,
                'assignment_stats': assignment_stats,
                'upcoming_activities': upcoming_activities,
            }
            return render(request, 'student/dashboard.html', context)
    
    return redirect('login')