from django.db import models
import uuid
from django.conf import settings
from django_resized import ResizedImageField


# post model
class Post(models.Model):
    post_id       = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    author        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_content  = models.TextField(blank=True, null=True)
    is_public     = models.BooleanField(default=False)
    created_date  = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self) -> str:
        return f'{self.author.username}\'s posts'

# image model
class PostImages(models.Model):
    image_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    images   = ResizedImageField(upload_to='images', size=[2680, None], blank=True, null=True)
    post     = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')
    
    def __str__(self) -> str:
        return f'{self.post.author.username} images'
    
# video model
class PostVideos(models.Model):
    video_id      = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    video         = models.FileField(upload_to='videos', null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    post          = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_video')
    
    def __str__(self) -> str:
        return f'{self.post.author.username} videos'
    
class PostComments(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    timestamp = models.DateTimeField(auto_now_add=True)

