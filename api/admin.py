
from api.models import Post,PostImages,PostVideos, PostComments
from semantic_forms.filters import SemanticFilterSet
from django.contrib import admin
from django.contrib.admin import ModelAdmin


class PostFilter(SemanticFilterSet):
    class Meta:
        model = Post
        fields = ("author", 'created_date')
        
class PostAdmin(ModelAdmin):
    list_display = ['post_id', 'author', 'post_content', 'created_date']
    list_filter = ['author', 'created_date']
    filterset_class = PostFilter

    
    class Meta:
        model = Post
        
class PostImageAdmin(ModelAdmin):
    list_display = ['post', 'semantic_autocomplete']
    list_filter = ['post']
    
    readonly_fields = ('semantic_autocomplete',)
    
    class Meta:
        model = PostImages
        
class PostCommentsAdmin(ModelAdmin):
    list_display = ['id', 'sender', 'comment', 'post', 'timestamp', 'parent', 'is_visible', 'is_deleted']
    list_filter = ['sender', 'post']
    
    class Meta:
        model = PostComments
        
class PostVideoAdmin(admin.ModelAdmin):
    list_display = ['post', 'semantic_autocomplete', 'date_uploaded']
    list_filter = ['post']
    
    readonly_fields = ('semantic_autocomplete',)
    
    class Meta:
        model = PostVideos

admin.site.register(Post, PostAdmin)
admin.site.register(PostImages, PostImageAdmin)
admin.site.register(PostVideos, PostVideoAdmin)
admin.site.register(PostComments, PostCommentsAdmin)

