from django.urls import path
from . import views


urlpatterns = [
    path('all/', views.view_all_room, name='all_room'),

    path('activity/<int:activity_id>/', views.activity_view, name='activity_view'),
    path('announcement/<int:announcement_id>/', views.announcement_view, name='announcement'),

    path('create/', views.create_room, name='create_room'),
    path('delete/<int:announcement_id>/', views.delete_room, name='delete_room'),
    path('enroll/', views.enroll_student, name='enroll_student'),
    
    path('activity/create/', views.create_activity, name='create_activity'),
    path('announcement/create/', views.create_announcement, name='create_announcement'),

    path('activity/submit/', views.submit_activity, name='submit_activity'),
    path('activity/grade/', views.grade_submission, name='grade_submission'),

    path('<str:room_id>/', views.room_view, name='room'),
]

