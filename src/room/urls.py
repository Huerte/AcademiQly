from django.urls import path
from . import views


urlpatterns = [
    path('all/', views.view_all_room, name='all_room'),

    path('activity/<int:activity_id>/', views.activity_view, name='activity_view'),
    path('announcement/<int:announcement_id>/', views.announcement_view, name='announcement'),

    path('create/', views.create_room, name='create_room'),
    path('delete/<int:room_id>/', views.delete_room, name='delete_room'),

    path('enroll/', views.enroll_student, name='enroll_student'),
    path('leave/<str:room_id>/', views.leave_room, name='leave_room'),
    path('remove_student/', views.unenroll_student, name='kick_student'),

    path('activity/create/', views.create_activity, name='create_activity'),
    path('announcement/create/', views.create_announcement, name='create_announcement'),

    path('activity/submit/', views.submit_activity, name='submit_activity'),
    path('activity/grade/', views.grade_submission, name='grade_submission'),

    path('export/grades/<int:room_id>/', views.export_grades, name='export_grades'),

    path('files/activity/<int:activity_id>/', views.serve_activity_resource, name='serve_activity_resource'),
    path('files/submission/<int:submission_id>/', views.serve_submission_file, name='serve_submission_file'),

    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/clear-all/', views.clear_all_notifications, name='clear_all_notifications'),

    path('video-call/<int:room_id>/', views.video_call_view, name='video_call'),

    path('<str:room_id>/', views.room_view, name='room'),
]
