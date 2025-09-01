from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('login/user/', views.login_user, name='login_user'),
    path('register/user/', views.register_user, name='register_user'),
]
