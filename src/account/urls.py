from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('login/user/', views.login_user, name='login_user'),
    path('register/user/', views.register_user, name='register_user'),
    path('profile/teacher/', views.profile_teacher, name='profile_teacher'),
    path('profile/student/', views.profile_student, name='profile_student'),
    path('view/teacher/<int:teacher_id>/', views.view_teacher_profile, name='view_teacher_profile'),
    path('view/student/<int:student_id>/', views.view_student_profile, name='view_student_profile'),
]
