from django.db.models.signals import post_save
from django.dispatch import receiver

from chat.serializers import ImageMessageSerializer, NotificationSerializer
from .models import AudioMessage, ImageMessage, Messages, MessageNotification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Messages)
def create_notification(instance, created, **kwargs):
    if created:
        message_notification = MessageNotification.objects.create(
            sender=instance.sender, 
            receiver=instance.receiver, 
            message=instance.message
        )
        
        # message_notification.save()
        
        serializer = NotificationSerializer(message_notification)
        
        data = serializer.data

        # Send the notification to the appropriate users via Django Channels
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications', 
            {
                'type': 'send_text_notification',
                'receiver': data['receiver']['user_id'], # receiver id
                'sender': data['sender']['username'], # sender user name
                'sender_id': data['sender']['user_id'],
                'avatar': data['sender']['avatar'], # sender avatar
                'notification': data['message'], # message content
                'timestamp': data['timestamp'],
                'message_type': 'text',
            }
        )
        
@receiver(post_save, sender=ImageMessage)
def create_iamge_notification(instance, created, **kwargs):
    if created:
        image_notification = MessageNotification.objects.create(
            sender=instance.sender,
            receiver=instance.receiver,
            message=instance.images,
        )
        
        serializer = NotificationSerializer(image_notification)
        
        data = serializer.data
        
        channel_layer = get_channel_layer()
        # send image notifications
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_image_notification',
                'receiver': data['receiver']['user_id'], # receiver id
                'sender': data['sender']['username'], # sender user name
                'sender_id': data['sender']['user_id'],
                'avatar': data['sender']['avatar'], # sender avatar
                'notification': data['message'], # message content
                'timestamp': data['timestamp'],
                'message_type': 'image',
            }
        )
        
# audio notifications
@receiver(post_save, sender=AudioMessage)
def create_audio_notification(instance, created, **kwargs):
    if created:
        
        audio_notify = MessageNotification.objects.create(
            sender = instance.sender,
            receiver = instance.receiver,
            message = instance.duration
        )
        
        serializer = NotificationSerializer(audio_notify)
        
        data = serializer.data
        
        channel_layer = get_channel_layer()
        
        async_to_sync(channel_layer.group_send)(
                'notifications',
                {
                    'type': 'send_audio_notification',
                    'receiver': data['receiver']['user_id'], # receiver id
                    'sender': data['sender']['username'], # sender user name
                    'sender_id': data['sender']['user_id'],
                    'avatar': data['sender']['avatar'], # sender avatar
                    'notification': data['message'], # message content
                    'timestamp': data['timestamp'],
                    'message_type': 'audio',
                }
            )