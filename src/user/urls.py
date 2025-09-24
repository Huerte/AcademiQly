from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('login-user/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('role-selection/', views.role_selection, name='role_selection'),
    path('select-role/', views.select_role, name='select_role'),
    path('setup/teacher/', views.teacher_setup, name='teacher_setup'),
    path('setup/student/', views.student_setup, name='student_setup'),
    path('view/<str:id>/', views.view_profile, name='view_profile'),
    path('settings/', views.user_settings, name='user_settings'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
