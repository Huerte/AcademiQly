from .models import Notification
from user.models import StudentProfile


def create_student_notifications(students, notification_type, title, message, **kwargs):
    notifications = []
    for student in students:
        notifications.append(Notification(
            recipient=student,
            notification_type=notification_type,
            title=title,
            message=message,
            **kwargs
        ))
    Notification.objects.bulk_create(notifications)


def create_teacher_notification(teacher_user, notification_type, title, message, **kwargs):
    Notification.create_notification(
        recipient=teacher_user,
        notification_type=notification_type,
        title=title,
        message=message,
        **kwargs
    )


def notify_activity_graded(submission):
    Notification.create_notification(
        recipient=submission.student.user,
        notification_type='activity_graded',
        title=f'Activity "{submission.activity.title}" Graded',
        message=f'Your submission has been graded. Score: {submission.score}/{submission.activity.total_marks}',
        room=submission.activity.room,
        activity=submission.activity,
        submission=submission
    )


def notify_new_activity(activity):
    students = activity.room.students.all()
    create_student_notifications(
        students=students,
        notification_type='new_activity',
        title=f'New Activity: {activity.title}',
        message=f'A new activity has been assigned in {activity.room.name}',
        room=activity.room,
        activity=activity
    )


def notify_student_submission(submission):
    create_teacher_notification(
        teacher_user=submission.activity.room.teacher.user,
        notification_type='student_submitted',
        title=f'New Submission from {submission.student.user.get_full_name()}',
        message=f'{submission.student.user.get_full_name()} submitted work for "{submission.activity.title}" in {submission.activity.room.name}',
        room=submission.activity.room,
        activity=submission.activity,
        submission=submission,
        related_user=submission.student.user
    )


def notify_student_enrolled(room, student):
    try:
        student_profile = StudentProfile.objects.get(user=student)
        create_teacher_notification(
            teacher_user=room.teacher.user,
            notification_type='student_enrolled',
            title=f'New Student Enrolled: {student.get_full_name()}',
            message=f'{student.get_full_name()} ({student_profile.course}) has enrolled in {room.name}',
            room=room,
            related_user=student
        )
    except StudentProfile.DoesNotExist:
        pass


def notify_student_left(room, student):
    try:
        student_profile = StudentProfile.objects.get(user=student)
        create_teacher_notification(
            teacher_user=room.teacher.user,
            notification_type='student_left',
            title=f'Student Left: {student.get_full_name()}',
            message=f'{student.get_full_name()} ({student_profile.course}) has left {room.name}',
            room=room,
            related_user=student
        )
    except StudentProfile.DoesNotExist:
        pass


def notify_activity_due_soon(activity, hours_until_due=24):
    from .models import Submission
    submitted_students = Submission.objects.filter(activity=activity).values_list('student__user', flat=True)
    pending_students = activity.room.students.exclude(id__in=submitted_students)
    
    create_student_notifications(
        students=pending_students,
        notification_type='activity_due_soon',
        title=f'Activity Due Soon: {activity.title}',
        message=f'"{activity.title}" is due in {hours_until_due} hours. Don\'t forget to submit!',
        room=activity.room,
        activity=activity
    )


def notify_activity_overdue(activity):
    from .models import Submission
    submitted_students = Submission.objects.filter(activity=activity).values_list('student__user', flat=True)
    pending_students = activity.room.students.exclude(id__in=submitted_students)
    
    create_student_notifications(
        students=pending_students,
        notification_type='activity_overdue',
        title=f'Activity Overdue: {activity.title}',
        message=f'"{activity.title}" is now overdue. Contact your teacher if you need assistance.',
        room=activity.room,
        activity=activity
    )
