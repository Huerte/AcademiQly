from django.db import models
from django.contrib.auth.models import User, AbstractUser


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    
    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=15)

    course = models.CharField(max_length=50)
    year_level = models.CharField(max_length=20)
    section = models.CharField(max_length=10)

    academic_interest = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)

    phone_number = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return f'{self.student_id} : {self.full_name}'

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')

    full_name = models.CharField(max_length=100)

    department = models.CharField(max_length=50)
    years_of_exp = models.CharField(max_length=20)
    highest_qualification = models.CharField(max_length=50)

    specialization = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)

    phone_number = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.full_name}'
