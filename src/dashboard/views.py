from django.shortcuts import render


def student_dashboard(request):
    return render(request, 'student_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')