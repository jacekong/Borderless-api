from django.db import models
import uuid
from django.conf import settings
from django_resized import ResizedImageField
from django.utils.html import format_html


# post model
class Post(models.Model):
    post_id       = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    author        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_content  = models.TextField(blank=True, null=True)
    is_public     = models.BooleanField(default=False)
    created_date  = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self) -> str:
        return f'{self.author.username}\'s post, posted on {self.created_date.strftime("%Y-%m-%d")}'
    
    class Meta:
        ordering = ('created_date',)

# image model
class PostImages(models.Model):
    image_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    images   = ResizedImageField(upload_to='images', size=[2680, None], blank=True, null=True)
    post     = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')
    
    def __str__(self) -> str:
        return f'{self.post.author.username} images'
    
    @property
    def semantic_autocomplete(self):
        if self.images:
            return format_html('<img src="{}" width="100" height="100" />'.format(self.images.url))
        return "No Image"

    semantic_autocomplete.fget.short_description = 'Image'
        
    
# video model
class PostVideos(models.Model):
    video_id      = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    video         = models.FileField(upload_to='videos', null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    post          = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_video')
    
    def __str__(self) -> str:
        return f'{self.post.author.username} video, posted on {self.date_uploaded.strftime("%Y-%m-%d")}'
    
    @property
    def semantic_autocomplete(self):
        if self.video:
            return format_html('<video src="{}" width="100" height="100" />'.format(self.video.url))
        return "No video"

    semantic_autocomplete.fget.short_description = 'Video'
    
class PostComments(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    is_visible = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('timestamp',)
        
    def __str__(self) -> str:
        return f'- {self.sender} comment on {self.post} -'
    
    @property
    def is_reply(self):
        return self.parent is not None

