from django.urls import path
from . import views


urlpatterns = [
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
]
