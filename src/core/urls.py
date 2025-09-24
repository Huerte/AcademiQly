from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),
    
    # Test error pages (remove in production)
    path('test-404/', views.test_404, name='test_404'),
    path('test-500/', views.test_500, name='test_500'),
    path('test-403/', views.test_403, name='test_403'),
]
