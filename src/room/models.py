import random
import string
import os
from django.db import models
from django.contrib.auth.models import User
from user.models import StudentProfile, TeacherProfile
from django.db import models


def generate_code():
    chars = string.ascii_lowercase + string.digits
    part1 = ''.join(random.choices(chars, k=3))
    part2 = ''.join(random.choices(chars, k=3))
    part3 = ''.join(random.choices(chars, k=4))
    return f"{part1}-{part2}-{part3}"


def activity_resource_upload_path(instance, filename):
    return f'activity_resources/room_{instance.room.id}/activity_{instance.id}/{filename}'


def submission_upload_path(instance, filename):
    return f'submissions/activity_{instance.activity.id}/student_{instance.student.user.id}/{filename}'


class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)

    students = models.ManyToManyField(User, related_name='students', blank=True)

    room_code = models.CharField(max_length=10, unique=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.room_code:
            code = generate_code()
            while Room.objects.filter(room_code=code).exists():
                code = generate_code()
            self.room_code = code

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Announcement(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Activity(models.Model):
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    resource_file = models.FileField(upload_to=activity_resource_upload_path, blank=True, null=True)

    total_marks = models.IntegerField(default=0)
    due_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("open", "Open"),
            ("closed", "Closed"),
        ],
        default="open",
    )

    class Meta:
        verbose_name_plural = 'Activities'

    def is_past_due(self):
        from django.utils import timezone
        return bool(self.due_date and self.due_date < timezone.now())

    def close_if_past_due(self, save=True):
        if self.is_past_due() and self.status != "closed":
            self.status = "closed"
            if save:
                self.save(update_fields=["status"])
            return True
        return False

    @classmethod
    def close_past_due_bulk(cls):
        from django.utils import timezone
        now = timezone.now()
        cls.objects.filter(due_date__isnull=False, due_date__lt=now).exclude(status="closed").update(status="closed")

    def get_resource_filename(self):
        if self.resource_file:
            return os.path.basename(self.resource_file.name)
        return None
    
    def is_image_resource(self):
        if self.resource_file:
            filename = self.resource_file.name.lower()
            return filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg'))
        return False

    def __str__(self):
        return self.title


class Submission(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)

    score = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    submission_file = models.FileField(upload_to=submission_upload_path, blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("submitted", "Submitted"),
            ("graded", "Graded"),
        ],
        default="submitted",
    )

    def get_submission_filename(self):
        if self.submission_file:
            return os.path.basename(self.submission_file.name)
        return None
    
    def is_image_submission(self):
        if self.submission_file:
            filename = self.submission_file.name.lower()
            return filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg'))
        return False

    def __str__(self):
        return f"{self.student.user.username} - {self.activity.title}"
    