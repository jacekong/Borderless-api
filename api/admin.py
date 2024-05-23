from django.contrib import admin
from api.models import Post,PostImages,PostVideos, PostComments

class PostAdmin(admin.ModelAdmin):
    list_display = ['post_id','author', 'post_content', 'created_date']
    list_filter = ['author', 'created_date']
    
    class Meta:
        models = Post
        
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['images', 'post']
    list_filter = ['post']
    
    class Meta:
        models = PostImages
        
class PostCommentsAdmin(admin.ModelAdmin):
    list_display = ['sender', 'comment', 'post', 'timestamp']
    list_filter = ['sender', 'post']
    
    class Meta:
        models = PostComments

admin.site.register(Post, PostAdmin)
admin.site.register(PostImages, PostImageAdmin)
admin.site.register(PostVideos)
admin.site.register(PostComments, PostCommentsAdmin)

