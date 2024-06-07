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

    
# get posts and create post
class PostsAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        request.data._mutable=True
        request.data['author_id'] = request.user.id

        post_serializer = PostSerializer(data=request.data, context={'request': request})
        
        if post_serializer.is_valid():
            
            post_serializer.save()  

            return Response(post_serializer.data, status=201)
        return Response(post_serializer.errors, status=400)

    # get post based on user's friends, can only friends be seen each other
    def get(self, request, format=None):
        user = request.user
        friends_list = FriendList.objects.filter(user=user)
        if friends_list.exists():
            friend_ids = friends_list.values_list('friends', flat=True)
            posts = Post.objects.filter(Q(author=user) | Q(author__id__in=friend_ids) | Q(is_public=False)).order_by('-created_date')
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


class GetRoutesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, rquest):
        routes = [
            {
                'user register': '/user/register'
            },
            {
                'update user': '/user/update/id'
            },
            {
                'get / create posts': '/api/posts'
            },
            {
                'single post': '/api/posts/id'
            },
            {
                "logged in user posts": 'api/posts/login/user'
            },
            {
                'get token / login': '/api/token/'
            },
            {
                'refresh token': '/api/token/refresh/'
            },
            {
                'logout': '/logout/'
            }
        ]
        
        return Response(routes, status=status.HTTP_200_OK)
