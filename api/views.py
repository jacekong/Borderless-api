from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Post, PostComments
from django.views.decorators.csrf import csrf_exempt
from friend.models import FriendList
from users.models import CustomUser
from .serializers import PostCommentSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q

from django.http import JsonResponse

from notification.models import Notification

# api 
# get posts and create post
class PostsAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data._mutable=True
        request.data['author_id'] = request.user.id

        post_serializer = PostSerializer(data=request.data, context={'request': request})
        
        if post_serializer.is_valid():
            
            post_serializer.save()

            return JsonResponse({'success': 'Post created successfully'}, status=status.HTTP_201_CREATED)
        return Response(post_serializer.errors, status=400)

    # get post based on user's friends, can only friends be seen each other
    def get(self, request, format=None):
        user = request.user
        friends_list = FriendList.objects.filter(user=user)
        if friends_list.exists():
            friend_ids = friends_list.values_list('friends', flat=True)
            posts = Post.objects.filter(Q(author=user) & Q(is_public=False) | Q(author__id__in=friend_ids) & Q(is_public=False)).order_by('-created_date')
        else:
            # If the user doesn't have friends, retrieve only their own posts
            posts = Post.objects.filter(Q(author=user) & Q(is_public=False)).order_by('-created_date')
            
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# get all the public posts   
class PublicPostAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        posts = Post.objects.filter(is_public=True).order_by('-created_date')
        
        serializer = PostSerializer(posts, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
            
# get logged in user's posts
class CurrentUserPostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        userId = request.user.id
        # Filter posts authored by the logged-in user
        user = get_object_or_404(CustomUser, id=userId)
        
        posts = Post.objects.filter(author=user).order_by('-created_date')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# get single post and delete single post  
class PostApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        
        post = get_object_or_404(Post ,post_id=pk)
        serializer = PostSerializer(post, context={'request': request})
        
        return Response(serializer.data)
    
    def delete(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, post_id=pk, author=user)
        post.delete()
        return Response({"message": "successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class PostCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        post = kwargs.get('pk')
        
        comments = PostComments.objects.filter(post=post)
        
        serializer = PostCommentSerializer(comments, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# get specific user's posts 
class SpecificUserPostsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        
        user = kwargs.get('user_id')
        
        view_user = CustomUser.objects.get(user_id=user)
        
        user_posts = Post.objects.filter(author=view_user)
        
        serializer = PostSerializer(user_posts, many=True, context={'request':request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        

# logout
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



# web
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

class Index(LoginRequiredMixin, View):
    N = 15
    context = {}
    
    def get(self, request):
        user = request.user
        friends_list = FriendList.objects.filter(user=user)
        if friends_list.exists():
            friend_ids = friends_list.values_list('friends', flat=True)
            posts_list = Post.objects.prefetch_related('post_images').filter(Q(author=user) | Q(author__id__in=friend_ids) | Q(is_public=True)).order_by('-created_date')

            # latest public posts
            public_posts = Post.objects.filter(is_public=True).order_by('-created_date')[:3] 
            # set pagination
            cookie_page = request.COOKIES.get('page')
            user_click_page = request.GET.get('page')
            
            if user_click_page:
                page = int(user_click_page)
            elif cookie_page:
                page = int(cookie_page)
            else:
                page = 1 
                
            paginator  = Paginator(posts_list, self.N, allow_empty_first_page=True)
            
            posts = paginator.get_page(page)
            
            self.context = {"posts": posts, "public_posts": public_posts}
            self.get_friends(user)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                current_path = request.headers.get('X-Current-Path', '')
                if current_path != '/':
                    html = render_to_string('partials/_posts_feed.html', self.context, request=request)
                else:
                    html = render_to_string('posts/posts_entire.html', self.context, request=request)

                return JsonResponse({
                    'html': html,
                    'has_next': posts.has_next(),
                    'page': page,
                })

            response = render(request, 'home/index.html', self.context)
            self.set_cookies(response, page)
            
            return response
        else:
            cookie_page = request.COOKIES.get('page')
            user_click_page = request.GET.get('page')
            
            if user_click_page:
                page = int(user_click_page)
            elif cookie_page:
                page = int(cookie_page)
            else:
                page = 1 

            posts_list = Post.objects.prefetch_related('post_images').filter(
                Q(author=user) | Q(is_public=True)
            ).order_by('-created_date')
            
            # latest public posts
            public_posts = Post.objects.filter(is_public=True).order_by('-created_date')[:3] 

            paginator = Paginator(posts_list, self.N, allow_empty_first_page=True)
            posts = paginator.get_page(page)

            self.context = {"posts": posts, "public_posts": public_posts}
            self.get_friends(user)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                current_path = request.headers.get('X-Current-Path', '')
                
                if current_path != '/':
                    html = render_to_string('partials/_posts_feed.html', self.context, request=request)
                else:
                    html = render_to_string('posts/posts_entire.html', self.context, request=request)
                    
                return JsonResponse({
                    'html': html,
                    'has_next': posts.has_next(),
                    'page': page,
                })
            response = render(request, 'home/index.html', self.context)
            self.set_cookies(response, page)
            
            return response
        
    def get_friends(self, user):
        try:
            friend_list = FriendList.objects.get(user=user.id)
            friends = friend_list.friends.all()
            # if not friends
            friend_ids = list(friends.values_list('id', flat=True)) 
            friend_ids.append(user.id)
            self.context.update({
                'friends': friend_ids
            })
        except FriendList.DoesNotExist:
            friend_ids = []
            # including login user
            friend_ids.append(user.id)
            self.context.update({
                'friends': friend_ids
            })
        
    def set_cookies(self, response, page):
        response.set_cookie('page', page)
        
class WebGetPostComments(LoginRequiredMixin, View):
    # get comments
    def get(self, request, post_id):
        post_comments = get_object_or_404(PostComments, post=post_id)
        
        return JsonResponse(post_comments)
    
class WebPostDetail(LoginRequiredMixin, View):
    template = 'posts/post_detail.html'
    
    def get(self, request, post_id):
        post = Post.objects.get(post_id=post_id)
        context = {'post': post}
        return render(request, self.template, context)
    
    
class WebRenderCreatePostTemplate(LoginRequiredMixin, View):
    template = 'posts/mobile_create_post.html'
    
    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(self.template, {})
            
            return JsonResponse({'html': html}, status=status.HTTP_200_OK)
        return render(request, 'posts/post_creation_template.html')
    
    
# ----------------------------------------------------------------
#  Liking machanism for post
# ----------------------------------------------------------------
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, post_id=post_id)
        if user in post.likes.all():
            # Unlike the post
            post.likes.remove(user)
            action = 'unliked'
        else:
            # Like the post
            post.likes.add(user)
            action = 'liked'
            # Notify the post owner (if not the same user)
            if post.author != user:
                Notification.objects.create(
                    user=post.author,
                    sender=user,
                    message=_(f"liked your post"),
                    type="like"
                )

        return JsonResponse({
            'status': 'success',
            'action': action,
            'like_count': post.likes.count()
        })
        
class WebLoadCommentsView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        page = 1
        post = Post.objects.get(post_id=post_id)
        comments = post.post_comments.all().order_by('-created_at')
        paginator = Paginator(comments, 10)
        page_obj = paginator.get_page(page)
        html = ''
        for comment in page_obj.object_list:
            if not comment.parent:
                html += render_to_string('partials/comment_block.html', {'comment': comment, 'post': post, 'level': 0}, request=request)
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next(),
        })