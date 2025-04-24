from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _

@login_required
def get_notifications(request):
    # Fetch unsent notifications
    unsent_notifications = Notification.objects.filter(user=request.user, is_sent=False)
    toast_data = [
        {
            'id': n.id,
            'message': n.message,
            'type': n.type,
            'created_at': n.created_at.isoformat(),
            'sender': {
                'username': n.sender.username,
                'user_id': n.sender.user_id,
                'avatar': n.sender.avatar.url if n.sender and n.sender.avatar else '/media/avatars/avatar.jpg'
            } if n.sender else None,
            'related_link': n.related_link,
        } for n in unsent_notifications
    ]
    unsent_notifications.update(is_sent=True)

    all_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    dropdown_data = [
        {
            'id': n.id,
            'message': n.message,
            'type': n.type,
            'created_at': n.created_at.isoformat(),
            'is_read': n.is_read,
            'sender': {
                'username': n.sender.username,
                'user_id': n.sender.user_id,
                'avatar': n.sender.avatar.url if n.sender and n.sender.avatar else '/media/avatars/avatar.jpg'
            } if n.sender else None,
            'related_link': n.related_link,
        } for n in all_notifications
    ]

    return JsonResponse({
        'toast_notifications': toast_data,
        'dropdown_notifications': dropdown_data,
    })

@login_required
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': _('Notification not found')}, status=404)
    
class WebNotificationsView(LoginRequiredMixin, View):
    
    def get(self, request):
        
        user = request.user
        
        notifications = Notification.objects.filter(user=user)
        
        context = {
            'notifications': notifications,
        }
    
        # Check if the request is from HTMX
        if request.headers.get('HX-Request') == 'true':
            return render(request, 'partials/_notifications.html', context)
        return render(request, 'notifications.html', context)