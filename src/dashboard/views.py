from django.shortcuts import render


def student_dashboard(request):
    return render(request, 'section/student_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'section/teacher_dashboard.html')