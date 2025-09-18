import random
import string
from django.db import models
from django.contrib.auth.models import User


def generate_code():
    chars = string.ascii_lowercase + string.digits
    part1 = ''.join(random.choices(chars, k=3))
    part2 = ''.join(random.choices(chars, k=3))
    part3 = ''.join(random.choices(chars, k=4))
    return f"{part1}-{part2}-{part3}"


class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    students = models.ManyToManyField(User, related_name='students', blank=True)

    room_code = models.CharField(max_length=10, unique=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.room_code:
            code = generate_code()
            while Room.objects.filter(room_code=self.room_code).exists():
                code = generate_code()
            self.room_code = code

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    
    
class Activity(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    resource = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    
class Announcement(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title