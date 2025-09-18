from django.urls import path
from . import views


urlpatterns = [
    path('all/', views.view_all_room, name='all_room'),

    path('activity/', views.activity_view, name='activity_view'),
    path('activity/student-edition', views.activity_view_s, name='activity_view_s'),

    path('create/', views.create_room, name='create_room'),
    path('enroll/', views.enroll_student, name='enroll_student'),
    path('announcement/', views.announcement_view, name='announcement'),

    path('<str:room_id>/', views.room_view, name='room'),
]

