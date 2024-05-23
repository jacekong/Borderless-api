from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Messages(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE,)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class AudioMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_audio', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_audio')
    audio_file = models.FileField(upload_to='audio_messages/')
    duration = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class ImageMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_image', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_image')
    images   = ResizedImageField(upload_to='image_messages/', size=[2680, None])
    timestamp = models.DateTimeField(auto_now_add=True)
     
class ChatList(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chats_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chats_as_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user1', 'user2']
        ordering = ['-updated_at']
        
    def __str__(self) -> str:
        return f'Chat between {self.user1.username} and {self.user2.username}'

    # use django signals to notify user that data has been changed
    # 1. data change from text message
    @receiver(post_save, sender=Messages)
    def update_chat_list(sender, instance, created, **kwargs):
        if created:
            user1 = instance.sender
            user2 = instance.receiver
            chat_list1, _ = ChatList.objects.get_or_create(user1=user1, user2=user2)
            chat_list2, _ = ChatList.objects.get_or_create(user1=user2, user2=user1)
            
            chat_list1.save()
            chat_list2.save()
            
    # 2. data change from image message
    @receiver(post_save, sender=ImageMessage)
    def update_chat_list_image(instance, created, **kwargs):
        if created:
            # get both user1 and user2
            user1 = instance.sender
            user2 = instance.receiver
            
            # update both chat_list1 and chat_list2
            chat_list1, _ = ChatList.objects.get_or_create(user1=user1, user2=user2)
            chat_list2, _ = ChatList.objects.get_or_create(user1=user2, user2=user1)
            
            # save instance
            chat_list1.save()
            chat_list2.save()
            
    # 3. update chat_list when receive or send audio message
    @receiver(post_save, sender=AudioMessage)
    def update_chat_list_image(instance, created, **kwargs):
        if created:
            # get both user1 and user2
            user1 = instance.sender
            user2 = instance.receiver
            
            # update both chat_list1 and chat_list2
            chat_list1, _ = ChatList.objects.get_or_create(user1=user1, user2=user2)
            chat_list2, _ = ChatList.objects.get_or_create(user1=user2, user2=user1)
            
            # save instance
            chat_list1.save()
            chat_list2.save()
            
class MessageNotification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

                