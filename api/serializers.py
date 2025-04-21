from rest_framework import serializers
from users.models import CustomUser
from users.serializers import UserSerializer
from .models import Post, PostImages, PostVideos, PostComments

from .tasks import transcode_video

class PostImagesSerializer(serializers.ModelSerializer):
    images = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)
    
    class Meta:
        model = PostImages
        fields = ('images',)
        
    def create(self, validated_data):
        image = validated_data.pop('images')
        if image:
            post_image = PostImages.objects.create(images=image, **validated_data)
            return post_image
        
        
class PostVideosSerializer(serializers.ModelSerializer):
    video = serializers.FileField(max_length=None, allow_empty_file=True, use_url=True)
    
    class Meta:
        model = PostVideos
        fields = ('video', 'video_id', 'processed', 'hls_path')
        
    def create(self, validated_data):
        video = validated_data.pop('video')
        if video:
            post_video = PostVideos.objects.create(video=video, **validated_data)
            return post_video
        
class PostCommentSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    
    class Meta:
        model = PostComments
        fields = ('id', 'sender','comment', 'post', 'timestamp', 'parent', 'is_visible', 'is_deleted')
        
        
class PostSerializer(serializers.ModelSerializer):
    post_images = PostImagesSerializer(many=True, read_only=True)
    post_video = PostVideosSerializer(many=True, read_only=True)
    post_comments = PostCommentSerializer(many=True, read_only=True)
    
    author = serializers.SerializerMethodField('get_author')
    
    class Meta:
        model = Post
        fields = ('post_id', 'post_content', 'created_date', 'modified_date', 'post_comments', 'post_images', 'post_video', 'author_id', 'author', 'is_public')

    def get_author(self, obj):
        author_id = obj.author_id  # Access the author_id from the Post object
        author = CustomUser.objects.get(pk=author_id)  # Retrieve the CustomUser instance
        avatar_url = None
        if author:
            avatar_url = author.avatar.url if author.avatar else None
            return {
                'user_id': author.user_id,
                'username': author.username,
                'avatar': self.context['request'].build_absolute_uri(avatar_url) if avatar_url else None
            }
        return None
        
    def create(self, validated_data):
        author_id = self.initial_data.get('author_id')
        author = CustomUser.objects.get(pk=author_id)
        images_data = self.context.get('request').FILES.getlist('post_images')
        video_data = self.context.get('request').FILES.get('post_video')
        
        post = Post.objects.create(author=author, **validated_data)
        
        if images_data:
            for image_data in images_data:
                PostImages.objects.create(post=post, images=image_data)
                
        if video_data:
            post_video = PostVideos.objects.create(post=post, video=video_data)
            transcode_video.delay(str(post_video.video_id))
            
        return post