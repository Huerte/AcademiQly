from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count
from django.db.models.functions import TruncMonth, ExtractYear
from core.mixins import AnalyticsAdminMixin
from .models import StudentProfile, TeacherProfile, Course, YearLevel, Qualification


admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(AnalyticsAdminMixin, BaseUserAdmin):
    chart_title = "User Registration Timeline"
    chart_type = "line"
    
    def get_chart_data(self, queryset):
        data = list(queryset.annotate(month=TruncMonth('date_joined')).values('month').annotate(count=Count('id')).order_by('month'))
        
        if not data:
             return {
                'labels': ['No Data'],
                'datasets': [{
                    'label': 'New Users',
                    'data': [0],
                    'backgroundColor': 'rgba(40, 167, 69, 0.2)',
                }]
            }

        labels = [x['month'].strftime('%Y-%m') for x in data] if data[0]['month'] else [] 

        if not labels and data:
             labels = ["Unknown"] * len(data)

        counts = [x['count'] for x in data]

        return {
            'labels': labels,
            'datasets': [{
                'label': 'New Users Joined',
                'data': counts,
                'backgroundColor': 'rgba(40, 167, 69, 0.2)',
                'borderColor': 'rgba(40, 167, 69, 1)',
                'borderWidth': 2,
                'fill': True,
                'tension': 0.4
            }]
        }

@admin.register(StudentProfile)
class StudentProfileAdmin(AnalyticsAdminMixin, admin.ModelAdmin):
    list_display = ('user', 'student_id', 'course', 'year_level')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id')
    list_filter = ('course', 'year_level')
    chart_title = "Students by Course"
    chart_type = "doughnut"

    def get_chart_data(self, queryset):
        data = list(queryset.values('course__name').annotate(count=Count('id')).order_by('-count'))
        
        if not data:
            return {
                'labels': ['No Students'],
                'datasets': [{
                    'data': [1],
                    'backgroundColor': ['#6c757d'],
                }]
            }
            
        labels = [x['course__name'] if x['course__name'] else 'No Course' for x in data]
        counts = [x['count'] for x in data]
        
        colors = ['#007bff', '#6610f2', '#6f42c1', '#e83e8c', '#dc3545', '#fd7e14', '#ffc107', '#28a745', '#20c997', '#17a2b8']
        
        return {
            'labels': labels,
            'datasets': [{
                'data': counts,
                'backgroundColor': colors[:len(labels)] if len(labels) <= len(colors) else colors * (len(labels) // len(colors) + 1),
            }]
        }

@admin.register(TeacherProfile)
class TeacherProfileAdmin(AnalyticsAdminMixin, admin.ModelAdmin):
    list_display = ('user', 'department', 'highest_qualification')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('department', 'highest_qualification')
    chart_title = "Teachers by Department"
    chart_type = "pie"

    def get_chart_data(self, queryset):
        data = list(queryset.values('department__name').annotate(count=Count('id')).order_by('-count'))
        
        if not data:
            return {
                'labels': ['No Teachers'],
                'datasets': [{
                    'data': [1],
                    'backgroundColor': ['#6c757d'],
                }]
            }

        labels = [x['department__name'] if x['department__name'] else 'No Department' for x in data]
        counts = [x['count'] for x in data]
        
        colors = ['#17a2b8', '#ffc107', '#28a745', '#007bff']

        return {
            'labels': labels,
            'datasets': [{
                'data': counts,
                'backgroundColor': colors[:len(labels)] if len(labels) <= len(colors) else colors * (len(labels) // len(colors) + 1),
            }]
        }

@admin.register(Course)
class CourseAdmin(AnalyticsAdminMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    chart_title = "Students per Course"
    chart_type = "bar"
    
    def get_chart_data(self, queryset):




        
        data = list(queryset.annotate(student_count=Count('studentprofile')).order_by('-student_count'))
        
        if not data:
             return {
                'labels': ['No Data'],
                'datasets': [{
                    'label': 'Students',
                    'data': [0],
                    'backgroundColor': 'rgba(52, 58, 64, 0.5)',
                }]
            }

        labels = [x.name for x in data]
        counts = [x.student_count for x in data]


        colors = [
            'rgba(255, 99, 132, 0.7)',   # Red
            'rgba(54, 162, 235, 0.7)',   # Blue
            'rgba(255, 206, 86, 0.7)',   # Yellow
            'rgba(75, 192, 192, 0.7)',   # Teal
            'rgba(153, 102, 255, 0.7)',  # Purple
            'rgba(255, 159, 64, 0.7)',   # Orange
            'rgba(199, 199, 199, 0.7)',  # Grey
            'rgba(83, 102, 255, 0.7)',   # Indigo
            'rgba(40, 167, 69, 0.7)',    # Green
            'rgba(23, 162, 184, 0.7)',   # Cyan
        ]


        if len(labels) <= len(colors):
            final_colors = colors[:len(labels)]
        else:
            final_colors = (colors * (len(labels) // len(colors) + 1))[:len(labels)]
            
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Enrolled Students',
                'data': counts,
                'backgroundColor': final_colors,
                'borderColor': [c.replace('0.7', '1') for c in final_colors],
                'borderWidth': 1
            }]
        }

@admin.register(YearLevel)
class YearLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('name',)
