from django.contrib import admin
from .models import Room, Activity, Announcement, Submission


admin.site.register(Room)
admin.site.register(Activity)
admin.site.register(Announcement)
admin.site.register(Submission)