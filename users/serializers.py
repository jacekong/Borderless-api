from rest_framework import serializers
from .models import CustomUser
from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, required=True)
    # avatar_url = serializers.SerializerMethodField()
    user_id = serializers.CharField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('user_id', 'username', 'bio', 'email', 'password', 'avatar')
        
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_avatar(self, obj):
        # Check if the avatar is not None
        if obj.avatar:
            # Construct the absolute URL for the avatar
            return self.context['request'].build_absolute_uri(obj.avatar.url)
        return None
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        avatar = validated_data.pop('avatar', None)
        
        # Generate user_id
        user = CustomUser(**validated_data)
        user.user_id = user._get_random_id()
            
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        if avatar:
            user.avatar = avatar
        user.save()
        
        return user
        
    
class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, required=False)
    email = serializers.EmailField(required=False) 
    avatar = serializers.ImageField(required=False) 
    
    class Meta:
        model = CustomUser
        fields = ('user_id', 'username', 'bio', 'email', 'password', 'avatar')
        
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    # def update(self, instance, validated_data):
    #     # Remove email and password fields if they are not provided in the validated data
    #     validated_data.pop('email', None)
    #     validated_data.pop('password', None)
        
    #     new_avatar = validated_data.pop('avatar', None)
    #     if new_avatar:
    #         instance.avatar = new_avatar

    #     return super().update(instance, validated_data)
    def update(self, instance, validated_data):
        # Perform partial update based on provided fields
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
        
        instance.save()
        return instance
    
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Customize token payload with user information
#         token['username'] = user.username
#         token['email'] = user.email
#         token['id'] = user.id

#         return token

#     def validate(self, attrs):
#         data = super().validate(attrs)
        
#         # Add user information to the response
#         data['username'] = self.user.username
#         data['email'] = self.user.email
#         data['user_id'] = self.user.id

#         return data