from django.urls import path
from . import views


urlpatterns = [
    path('', views.room_view, name='room'),
    path('all/', views.all_room, name='all_room'),

    path('student-edition/', views.room_view_s, name='room_s'),
    path('all/student-edition', views.all_room_s, name='all_room_s'),

    path('activity/', views.activity_view, name='activity_view'),
    path('activity/student-edition', views.activity_view_s, name='activity_view_s'),


    path('announcement/', views.announcement_view, name='announcement'),

]
