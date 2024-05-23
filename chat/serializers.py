from rest_framework import serializers
from users.serializers import UserSerializer
from .models import AudioMessage, MessageNotification, Messages, ChatList, ImageMessage

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    
    class Meta:
        model = Messages
        fields = ['sender', 'receiver', 'message', 'timestamp']
        

class ChatListSerializer(serializers.ModelSerializer):
    user1 = UserSerializer()
    user2 = UserSerializer()

    class Meta:
        model = ChatList
        fields = ['id', 'user1', 'user2', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        

class ImageMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    
    class Meta:
        model = ImageMessage
        fields = ['sender', 'receiver', 'images', 'timestamp']
        
    def get_image(self, obj):
        if obj.images:
            return self.context['request'].build_absolute_uri(obj.images)
        
class AudioMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    
    class Meta:
        model = AudioMessage
        fields = ['sender', 'receiver', 'audio_file', 'duration', 'timestamp']
        
    def get_audio(self, obj):
        if obj.audio:
            return self.context['request'].build_absolute_uri(obj.audio)
        
class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    
    class Meta:
        model = MessageNotification
        fields = ['sender', 'receiver', 'message', 'read', 'timestamp']
    
        
        