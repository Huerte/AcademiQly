from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('login/user/', views.login_user, name='login_user'),
    path('register/user/', views.register_user, name='register_user'),
    path('setup/teacher/', views.teacher_setup, name='teacher_setup'),
    path('setup/student/', views.student_setup, name='student_setup'),
    path('view/teacher/', views.view_teacher_profile, name='view_teacher_profile'),
    path('view/student/', views.view_student_profile, name='view_student_profile'),
]
