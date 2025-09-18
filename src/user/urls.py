from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('role-selection/', views.role_selection, name='role_selection'),
    path('select-role/', views.select_role, name='select_role'),
    path('setup/teacher/', views.teacher_setup, name='teacher_setup'),
    path('setup/student/', views.student_setup, name='student_setup'),
    path('view/teacher/', views.view_teacher_profile, name='view_teacher_profile'),
    path('view/student/', views.view_student_profile, name='view_student_profile'),
]
