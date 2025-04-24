from django.db import models
from users.models import CustomUser

class Notification(models.Model):
    TYPE_CHOICES = (
        ('success', 'Success'),
        ('error', 'Error'),
        ('info', 'Info'),
        ('message', 'Message'),
        ('friend_request', 'Friend Request'),
        ('like', 'Like'),
        ('comment', 'Comment')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_notifications')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    message = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    related_link = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} for {self.user.username}"