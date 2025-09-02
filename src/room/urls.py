from django.urls import path
from . import views


urlpatterns = [
    path('', views.room_view, name='room'),
    path('all/', views.all_room, name='all_room'),

    path('student-edition/', views.room_view_s, name='room_s'),
    path('all/student-edition', views.all_room_s, name='all_room_s'),
]
