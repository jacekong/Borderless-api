from django_sendfile import sendfile
from django.http import Http404
from django.shortcuts import get_object_or_404
from pathlib import Path
from django.conf import settings

from api.models import Post, PostVideos
from friend.models import FriendList


def serve_media(request, path):
    # Construct the full file path
    file_path = Path(settings.MEDIA_ROOT) / path
    if not file_path.exists():
        raise Http404("Media file not found")
    # Determine the type of media file
    if path.startswith('post_images/'):
        post_id = path.split('/')[1]
        post = get_object_or_404(Post, post_id=post_id)

        # Allow access if:
        # 1. Post is public
        # 2. User is the author
        # 3. User is a friend of the author (if post is private)
        if not request.user.is_authenticated:
            raise Http404("Authentication required")
        
        if post.is_public:
            return sendfile(request, path)

        if post.author == request.user:
            return sendfile(request, path)

        # Check if the user is a friend of the author
        if FriendList.objects.filter(user=post.author, friends=request.user).exists() or \
           FriendList.objects.filter(user=request.user, friends=post.author).exists():
            return sendfile(request, path)

        raise Http404("You do not have permission to access this media")

    elif path.startswith('user_avatars/'):
        # Allow access if:
        # 1. User is authenticated
        if not request.user.is_authenticated:
            raise Http404("Authentication required")

        if request.user.is_authenticated:
            return sendfile(request, path)

        raise Http404("You do not have permission to access this avatar")
    
    elif path.startswith('avatars/'):
        # Allow access if:
        # 1. User is authenticated
        if not request.user.is_authenticated:
            raise Http404("Authentication required")

        if request.user.is_authenticated:
            return sendfile(request, path)

        raise Http404("You do not have permission to access this avatar")
    
    elif path.startswith('videos/'):
        video_id = path.split('/')[1]
        post_video = get_object_or_404(PostVideos, video_id=video_id)
        post = get_object_or_404(Post, post_id=post_video.post.post_id)
        # Allow access if:
        # 1. Post is public
        # 2. User is the author
        # 3. User is a friend of the author (if post is private)
        if not request.user.is_authenticated:
            raise Http404("Authentication required")
        
        if post.is_public:
            return sendfile(request, path)

        if post.author == request.user:
            return sendfile(request, path)

        # Check if the user is a friend of the author
        if FriendList.objects.filter(user=post.author, friends=request.user).exists() or \
           FriendList.objects.filter(user=request.user, friends=post.author).exists():
            return sendfile(request, path)

        raise Http404("You do not have permission to access this media")

    raise Http404("Invalid media path")