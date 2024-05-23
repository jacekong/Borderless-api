from rest_framework import serializers
from .models import FriendList, FriendRequest
from users.serializers import UserSerializer

class FriendListSerializer(serializers.ModelSerializer):
    friends = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = FriendList
        fields = ['friends']
    
    def get_user_data(self, user):
        if user:
            return {
                'user_id': user.user_id,
                'username': user.username,
                'bio': user.bio,
                'email': user.email,
                'avatar': self.context['request'].build_absolute_uri(user.avatar.url) if user.avatar else None
            }
        return None
        
class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['sender', 'receiver', 'is_active', 'timestamp']

    def get_sender(self, obj):
        return self.get_user_data(obj.sender)

    def get_receiver(self, obj):
        return self.get_user_data(obj.receiver)

    def get_user_data(self, user):
        if user:
            return {
                'user_id': user.user_id,
                'username': user.username,
                'bio': user.bio,
                'email': user.email,
                'avatar': self.context['request'].build_absolute_uri(user.avatar.url) if user.avatar else None
            }
        return None

        
        