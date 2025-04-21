
from api.models import Post,PostImages,PostVideos, PostComments
from semantic_forms.filters import SemanticFilterSet
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html

# Admin Panel ----------------------------------------------------------------
class PostImageInline(admin.TabularInline):
    model = PostImages
    extra = 0
    
    readonly_fields = ['image_preview']
    fields = ['images', 'image_preview']
    can_delete = True
    
    def image_preview(self, obj):
        if obj.images:
            return format_html('<img src="{}" width="100" height="100" />', obj.images.url)
        return "No Image"
    
    image_preview.short_description = "Preview"
    
class PostVideoInline(admin.TabularInline):
    extra = 0
    model = PostVideos
    
    readonly_fields = ['video_preview']
    fields = ['video', 'video_preview']
    can_delete = True
    
    def video_preview(self, obj):
        if obj.images:
            return format_html('<img src="{}" width="100" height="100" />', obj.images.url)
        return "No Video"
    
    video_preview.short_description = "Preview"

class PostFilter(SemanticFilterSet):
    class Meta:
        model = Post
        fields = ("author", 'is_public', 'created_date')
        
class PostAdmin(ModelAdmin):
    list_display = ['author', 'post_content', 'display_images', 'display_video', 'is_public', 'created_date']
    list_filter = ['author', 'is_public', 'created_date']
    filterset_class = PostFilter

    inlines = [PostImageInline, PostVideoInline]
    actions = ['make_post_public', 'make_post_private']
    
    class Meta:
        model = Post
        
    def display_images(self, obj):
        return format_html(''.join([
            f'<img src="{img.images.url}" width="50" height="50" style="margin:2px;" />'
            for img in obj.post_images.all()
        ]))
    display_images.short_description = "Images"
    
    def display_video(self, obj):
        return format_html(''.join([
            f'<img src="{img.video.url}" width="50" height="50" style="margin:2px;" />'
            for img in obj.post_video.all()
        ]))
    display_video.short_description = "Video"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('post_images', 'post_video')
        
    @admin.action(description="Make posts publicly")
    def make_post_public(self, request, queryset):
        queryset.update(is_public=True)

    @admin.action(description="Make posts private")
    def make_post_private(self, request, queryset):
        queryset.update(is_public=False)
        
class PostCommentsAdmin(ModelAdmin):
    list_display = ['id', 'sender', 'comment', 'post', 'timestamp', 'parent', 'is_visible', 'is_deleted']
    list_filter = ['sender', 'post']
    
    class Meta:
        model = PostComments

admin.site.register(Post, PostAdmin)
admin.site.register(PostComments, PostCommentsAdmin)