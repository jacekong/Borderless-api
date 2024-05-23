from django.contrib import admin
from .models import MessageNotification, Messages, ChatList, AudioMessage, ImageMessage

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'timestamp']
    list_filter = ['sender', 'timestamp']
    
    class Meta:
        models = Messages
        
class ChatListAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2', 'created_at', 'updated_at']
    list_filter = ['user1', 'user2', 'created_at']
    
    class Meta:
        models = ChatList
        
class AudioAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'duration', 'audio_file', 'timestamp']
    list_filter = ['sender']
    
    class Meta:
        models = AudioMessage
        
class ImageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'images', 'timestamp']
    list_filter = ['sender', 'receiver']
    
    class Meta:
        models = ImageMessage
        
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'read', 'timestamp']
    list_filter = ['sender', 'receiver']
    
    class Meta:
        models = MessageNotification
        
     
admin.site.register(Messages, MessageAdmin)
admin.site.register(ChatList, ChatListAdmin)
admin.site.register(AudioMessage, AudioAdmin)
admin.site.register(ImageMessage, ImageAdmin)
admin.site.register(MessageNotification, NotificationAdmin)