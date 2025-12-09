from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDay
from core.mixins import AnalyticsAdminMixin
from .models import Room, Activity, Announcement, Submission

@admin.register(Room)
class RoomAdmin(AnalyticsAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'teacher', 'room_code', 'created_at', 'get_student_count')
    search_fields = ('name', 'description', 'room_code', 'teacher__user__username')
    list_filter = ('created_at', 'teacher')
    chart_title = "Rooms by Creation Date"
    chart_type = "line"

    def get_student_count(self, obj):
        return obj.students.count()
    get_student_count.short_description = 'Students'

    def get_chart_data(self, queryset):
        data = list(queryset.annotate(date=TruncDay('created_at')).values('date').annotate(count=Count('id')).order_by('date'))
        
        if not data:
            return {
                'labels': ['No Data'],
                'datasets': [{
                    'label': 'New Rooms',
                    'data': [0],
                    'backgroundColor': 'rgba(60, 141, 188, 0.2)',
                    'borderColor': 'rgba(60, 141, 188, 1)',
                    'borderWidth': 2,
                    'fill': True,
                    'tension': 0.4
                }]
            }
        
        labels = [x['date'].strftime('%Y-%m-%d') for x in data]
        counts = [x['count'] for x in data]

        return {
            'labels': labels,
            'datasets': [{
                'label': 'New Rooms',
                'data': counts,
                'backgroundColor': 'rgba(60, 141, 188, 0.2)',
                'borderColor': 'rgba(60, 141, 188, 1)',
                'borderWidth': 2,
                'fill': True,
                'tension': 0.4
            }]
        }

@admin.register(Activity)
class ActivityAdmin(AnalyticsAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'room', 'status', 'due_date', 'total_marks')
    search_fields = ('title', 'description', 'room__name')
    list_filter = ('status', 'created_at', 'due_date', 'room')
    chart_title = "Activity Status Distribution"
    chart_type = "doughnut"

    def get_chart_data(self, queryset):
        data = list(queryset.values('status').annotate(count=Count('id')).order_by('status'))
        
        if not data:
            return {
                'labels': ['No Activities'],
                'datasets': [{
                    'data': [1],
                    'backgroundColor': ['#6c757d'],
                }]
            }
        
        labels = [x['status'].title() for x in data]
        counts = [x['count'] for x in data]
        

        colors = ['#28a745', '#dc3545', '#ffc107', '#17a2b8']
        
        return {
            'labels': labels,
            'datasets': [{
                'data': counts,
                'backgroundColor': colors[:len(labels)],
            }]
        }

@admin.register(Submission)
class SubmissionAdmin(AnalyticsAdminMixin, admin.ModelAdmin):
    list_display = ('student', 'activity', 'status', 'score', 'submitted_at')
    search_fields = ('student__user__username', 'activity__title')
    list_filter = ('status', 'submitted_at', 'activity__room')
    chart_title = "Submission Status"
    chart_type = "pie"

    def get_chart_data(self, queryset):
        data = list(queryset.values('status').annotate(count=Count('id')).order_by('status'))
        
        if not data:
            return {
                'labels': ['No Submissions'],
                'datasets': [{
                    'data': [1],
                    'backgroundColor': ['#6c757d'],
                }]
            }
        
        labels = [x['status'].title() for x in data]
        counts = [x['count'] for x in data]
        
        return {
            'labels': labels,
            'datasets': [{
                'data': counts,
                'backgroundColor': ['#007bff', '#6c757d', '#28a745'],
            }]
        }

@admin.register(Announcement)
class AnnouncementAdmin(AnalyticsAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'room', 'created_at')
    search_fields = ('title', 'content', 'room__name')
    list_filter = ('created_at', 'room')
    chart_title = "Announcements per Room"
    chart_type = "bar"

    def get_chart_data(self, queryset):

        data = list(queryset.values('room__name').annotate(count=Count('id')).order_by('-count')[:10])
        
        if not data:
             return {
                'labels': ['No Data'],
                'datasets': [{
                    'label': 'Announcements',
                    'data': [0],
                    'backgroundColor': 'rgba(23, 162, 184, 0.5)',
                }]
            }

        labels = [x['room__name'] for x in data]
        counts = [x['count'] for x in data]

        return {
            'labels': labels,
            'datasets': [{
                'label': 'Number of Announcements',
                'data': counts,
                'backgroundColor': 'rgba(23, 162, 184, 0.7)',
                'borderColor': 'rgba(23, 162, 184, 1)',
                'borderWidth': 1
            }]
        }