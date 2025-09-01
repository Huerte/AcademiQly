from django.urls import path
from . import views


urlpatterns = [
    path('', views.room_view, name='room'),
    path('all/', views.all_room, name='all_room')
]
