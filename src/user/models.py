from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class YearLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Qualification(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    student_id = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/students/', null=True, blank=True, default='profile_pics/default-profile.png')
    
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    year_level = models.ForeignKey(YearLevel, on_delete=models.SET_NULL, null=True, blank=True)

    academic_interest = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.student_id} : {self.user.get_full_name()}'

    def get_full_name(self):
        return f'{self.user.first_name} {self.middle_name or ""} {self.user.last_name}'



class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/teacher/', null=True, blank=True, default='profile_pics/default-profile.png') 

    department = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    highest_qualification = models.ForeignKey(Qualification, on_delete=models.SET_NULL, null=True, blank=True)

    years_of_exp = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    def get_full_name(self):
        return f'{self.user.first_name} {self.middle_name or ""} {self.user.last_name}'
