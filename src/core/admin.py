from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path
from django.db.models import Count, Avg, Q, F, IntegerField
from django.db.models.functions import TruncMonth, Cast
from django.utils import timezone
from datetime import timedelta
import json


from user.models import StudentProfile, TeacherProfile, Course
from room.models import Room, Activity, Submission


def get_analytics_data():
    avg_passing_result = Room.objects.aggregate(avg=Avg('base_passing'))
    PASSING_THRESHOLD = round(avg_passing_result['avg'], 0) if avg_passing_result['avg'] else 60
    

    total_students = StudentProfile.objects.count()
    total_teachers = TeacherProfile.objects.count()
    total_rooms = Room.objects.count()
    total_activities = Activity.objects.count()
    total_submissions = Submission.objects.count()
    

    graded_submissions = Submission.objects.filter(
        score__isnull=False,
        activity__total_marks__gt=0
    ).select_related('activity', 'activity__room')
    total_grades = graded_submissions.count()
    

    submission_percentages = []
    passing_count = 0
    failing_count = 0
    
    for sub in graded_submissions:
        if sub.activity.total_marks > 0:
            percentage = (sub.score / sub.activity.total_marks) * 100
            submission_percentages.append(percentage)

            room_threshold = sub.activity.room.base_passing if sub.activity.room else PASSING_THRESHOLD
            if percentage >= room_threshold:
                passing_count += 1
            else:
                failing_count += 1
    

    average_score = round(sum(submission_percentages) / len(submission_percentages), 2) if submission_percentages else 0
    

    pass_rate = round((passing_count / total_grades * 100), 2) if total_grades > 0 else 0
    failing_rate = round((failing_count / total_grades * 100), 2) if total_grades > 0 else 0
    

    twelve_months_ago = timezone.now() - timedelta(days=365)
    monthly_submissions = graded_submissions.filter(submitted_at__gte=twelve_months_ago)
    

    monthly_data = {}
    for sub in monthly_submissions:
        if sub.activity.total_marks > 0:
            month_key = sub.submitted_at.strftime('%Y-%m')
            percentage = (sub.score / sub.activity.total_marks) * 100
            if month_key not in monthly_data:
                monthly_data[month_key] = []
            monthly_data[month_key].append(percentage)
    

    monthly_avg_scores = []
    labels_months = []
    for month_key in sorted(monthly_data.keys()):
        month_date = timezone.datetime.strptime(month_key, '%Y-%m')
        labels_months.append(month_date.strftime('%b %Y'))
        monthly_avg_scores.append(round(sum(monthly_data[month_key]) / len(monthly_data[month_key]), 2))
    

    room_percentages = {}
    for sub in graded_submissions:
        if sub.activity.total_marks > 0 and sub.activity.room:
            room_name = sub.activity.room.name
            percentage = (sub.score / sub.activity.total_marks) * 100
            if room_name not in room_percentages:
                room_percentages[room_name] = []
            room_percentages[room_name].append(percentage)
    

    room_avg_list = [
        (room_name, round(sum(scores) / len(scores), 2))
        for room_name, scores in room_percentages.items()
    ]
    room_avg_list.sort(key=lambda x: x[1], reverse=True)
    top_rooms = room_avg_list[:10]
    
    subject_labels = [room[0] for room in top_rooms]
    subject_avg_scores = [room[1] for room in top_rooms]
    

    grade_distribution = {
        'A (90-100%)': 0,
        'B (80-89%)': 0,
        'C (70-79%)': 0,
        'D (60-69%)': 0,
        'F (<60%)': 0,
    }
    
    for percentage in submission_percentages:
        if percentage >= 90:
            grade_distribution['A (90-100%)'] += 1
        elif percentage >= 80:
            grade_distribution['B (80-89%)'] += 1
        elif percentage >= 70:
            grade_distribution['C (70-79%)'] += 1
        elif percentage >= 60:
            grade_distribution['D (60-69%)'] += 1
        else:
            grade_distribution['F (<60%)'] += 1
    
    grade_labels = list(grade_distribution.keys())
    grade_counts = list(grade_distribution.values())
    

    pass_fail_counts = [passing_count, failing_count]
    

    student_percentages = {}
    for sub in graded_submissions:
        if sub.activity.total_marks > 0:
            student_key = sub.student.id
            percentage = (sub.score / sub.activity.total_marks) * 100
            if student_key not in student_percentages:
                student_percentages[student_key] = {
                    'name': f"{sub.student.user.first_name} {sub.student.user.last_name}",
                    'student_id': sub.student.student_id,
                    'scores': []
                }
            student_percentages[student_key]['scores'].append(percentage)
    

    student_avg_list = []
    for student_id, data in student_percentages.items():
        if len(data['scores']) > 0:
            avg_percentage = round(sum(data['scores']) / len(data['scores']), 2)
            student_avg_list.append({
                'name': data['name'],
                'student_id': data['student_id'],
                'avg_score': avg_percentage,
                'submission_count': len(data['scores'])
            })
    
    student_avg_list.sort(key=lambda x: x['avg_score'], reverse=True)
    top_students_list = student_avg_list[:10]
    

    recent_grades = (
        graded_submissions
        .select_related('student__user', 'activity__room', 'activity')
        .order_by('-submitted_at')[:15]
    )
    
    recent_grades_list = [
        {
            'student_name': f"{sub.student.user.first_name} {sub.student.user.last_name}",
            'activity_title': sub.activity.title,
            'room_name': sub.activity.room.name,
            'score': sub.score,
            'total_marks': sub.activity.total_marks,
            'percentage': round((sub.score / sub.activity.total_marks * 100), 2) if sub.activity.total_marks > 0 else 0,
            'submitted_at': sub.submitted_at.strftime('%Y-%m-%d %H:%M')
        }
        for sub in recent_grades
    ]
    

    median_score = 0
    stddev_score = 0
    
    if submission_percentages:
        sorted_percentages = sorted(submission_percentages)
        n = len(sorted_percentages)
        if n > 0:

            if n % 2 == 0:
                median_score = (sorted_percentages[n//2 - 1] + sorted_percentages[n//2]) / 2
            else:
                median_score = sorted_percentages[n//2]
            

            mean = sum(submission_percentages) / n
            variance = sum((x - mean) ** 2 for x in submission_percentages) / n
            stddev_score = variance ** 0.5
    
    median_score = round(median_score, 2)
    stddev_score = round(stddev_score, 2)
    

    now = timezone.now()
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = this_month_start - timedelta(seconds=1)
    
    this_month_subs = graded_submissions.filter(submitted_at__gte=this_month_start)
    this_month_percentages = [
        (sub.score / sub.activity.total_marks) * 100
        for sub in this_month_subs
        if sub.activity.total_marks > 0
    ]
    this_month_avg = round(sum(this_month_percentages) / len(this_month_percentages), 2) if this_month_percentages else 0
    this_month_count = len(this_month_percentages)
    
    last_month_subs = graded_submissions.filter(
        submitted_at__gte=last_month_start,
        submitted_at__lte=last_month_end
    )
    last_month_percentages = [
        (sub.score / sub.activity.total_marks) * 100
        for sub in last_month_subs
        if sub.activity.total_marks > 0
    ]
    last_month_avg = round(sum(last_month_percentages) / len(last_month_percentages), 2) if last_month_percentages else 0
    last_month_count = len(last_month_percentages)
    

    improvement_rate = 0
    improvement_rate_valid = False
    
    if last_month_avg > 0 and this_month_avg > 0:

        improvement_rate = round(((this_month_avg - last_month_avg) / last_month_avg) * 100, 2)
        improvement_rate_valid = True
    elif last_month_avg > 0 and this_month_avg == 0 and this_month_count == 0:

        improvement_rate = 0
        improvement_rate_valid = False
    elif last_month_avg == 0 and this_month_avg > 0:

        improvement_rate = 100.0
        improvement_rate_valid = True
    else:

        improvement_rate = 0
        improvement_rate_valid = False
    

    

    teachers_by_department = (
        TeacherProfile.objects
        .select_related('department')
        .values('department__name')
        .annotate(count=Count('id'))
        .filter(department__name__isnull=False)
        .order_by('-count')
    )
    
    teacher_dept_labels = [item['department__name'] for item in teachers_by_department]
    teacher_dept_counts = [item['count'] for item in teachers_by_department]
    

    active_teachers = (
        Room.objects
        .select_related('teacher__user')
        .values('teacher__user__first_name', 'teacher__user__last_name', 'teacher__id')
        .annotate(
            room_count=Count('id'),
            activity_count=Count('activities'),
            student_count=Count('students', distinct=True)
        )
        .order_by('-room_count')[:10]
    )
    
    active_teachers_list = [
        {
            'name': f"{item['teacher__user__first_name']} {item['teacher__user__last_name']}",
            'room_count': item['room_count'],
            'activity_count': item['activity_count'],
            'student_count': item['student_count']
        }
        for item in active_teachers
    ]
    

    teacher_avg_scores = {}
    for sub in graded_submissions:
        if sub.activity.total_marks > 0 and sub.activity.room.teacher:
            teacher_id = sub.activity.room.teacher.id
            percentage = (sub.score / sub.activity.total_marks) * 100
            if teacher_id not in teacher_avg_scores:
                teacher_avg_scores[teacher_id] = {
                    'name': sub.activity.room.teacher.get_full_name(),
                    'scores': []
                }
            teacher_avg_scores[teacher_id]['scores'].append(percentage)
    

    teacher_performance_list = []
    for teacher_id, data in teacher_avg_scores.items():
        if len(data['scores']) > 0:
            avg_percentage = round(sum(data['scores']) / len(data['scores']), 2)
            teacher_performance_list.append({
                'name': data['name'],
                'avg_score': avg_percentage,
                'submission_count': len(data['scores'])
            })
    
    teacher_performance_list.sort(key=lambda x: x['avg_score'], reverse=True)
    top_teachers_list = teacher_performance_list[:10]
    

    teacher_grading_activity = {}
    for sub in graded_submissions:
        if sub.activity.room.teacher:
            teacher_id = sub.activity.room.teacher.id
            if teacher_id not in teacher_grading_activity:
                teacher_grading_activity[teacher_id] = {
                    'name': sub.activity.room.teacher.get_full_name(),
                    'graded_count': 0,
                    'pending_count': 0
                }
            if sub.score is not None:
                teacher_grading_activity[teacher_id]['graded_count'] += 1
            else:
                teacher_grading_activity[teacher_id]['pending_count'] += 1
    
    total_graded_by_teachers = sum(t['graded_count'] for t in teacher_grading_activity.values())
    total_pending_by_teachers = sum(t['pending_count'] for t in teacher_grading_activity.values())
    

    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_rooms = Room.objects.filter(created_at__gte=thirty_days_ago).count()
    recent_activities = Activity.objects.filter(created_at__gte=thirty_days_ago).count()
    

    avg_rooms_per_teacher = round(total_rooms / total_teachers, 2) if total_teachers > 0 else 0
    

    avg_activities_per_teacher = round(total_activities / total_teachers, 2) if total_teachers > 0 else 0
    

    total_enrollments = sum(room.students.count() for room in Room.objects.all())
    avg_students_per_teacher = round(total_enrollments / total_teachers, 2) if total_teachers > 0 else 0
    

    return {

        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_rooms': total_rooms,
        'total_activities': total_activities,
        'total_grades': total_grades,
        'average_score': average_score,
        'pass_rate': pass_rate,
        'failing_rate': failing_rate,
        'median_score': median_score,
        'stddev_score': stddev_score,
        'improvement_rate': improvement_rate,
        'improvement_rate_valid': improvement_rate_valid,
        

        'avg_rooms_per_teacher': avg_rooms_per_teacher,
        'avg_activities_per_teacher': avg_activities_per_teacher,
        'avg_students_per_teacher': avg_students_per_teacher,
        'total_graded_by_teachers': total_graded_by_teachers,
        'total_pending_by_teachers': total_pending_by_teachers,
        'recent_rooms': recent_rooms,
        'recent_activities': recent_activities,
        

        'monthly_avg_json': json.dumps(monthly_avg_scores),
        'labels_months_json': json.dumps(labels_months),
        'subject_labels_json': json.dumps(subject_labels),
        'subject_avg_scores_json': json.dumps(subject_avg_scores),
        'grade_labels_json': json.dumps(grade_labels),
        'grade_counts_json': json.dumps(grade_counts),
        'pass_fail_counts_json': json.dumps(pass_fail_counts),
        'teacher_dept_labels_json': json.dumps(teacher_dept_labels),
        'teacher_dept_counts_json': json.dumps(teacher_dept_counts),
        

        'top_students': top_students_list,
        'recent_grades': recent_grades_list,
        'active_teachers': active_teachers_list,
        'top_teachers': top_teachers_list,
        

        'passing_threshold': PASSING_THRESHOLD,
    }


@staff_member_required
def analytics_dashboard_view(request):
    context = get_analytics_data()
    return render(request, 'admin/analytics_dashboard.html', context)



_original_index = admin.site.index

def custom_admin_index(request, extra_context=None):

    extra_context = extra_context or {}

    extra_context.update(get_analytics_data())
    return _original_index(request, extra_context)

admin.site.index = custom_admin_index


_original_get_urls = admin.site.get_urls

def get_urls_with_analytics():

    urls = _original_get_urls()
    analytics_url = path('analytics/', admin.site.admin_view(analytics_dashboard_view), name='analytics_dashboard')
    return [analytics_url] + urls

admin.site.get_urls = get_urls_with_analytics
