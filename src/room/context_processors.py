from .models import Notification


def notification_context(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).count()
        
        recent_notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by('-created_at')[:5]
        
        return {
            'notification_count': unread_count,
            'recent_notifications': recent_notifications
        }
    
    return {
        'notification_count': 0,
        'recent_notifications': []
    }
