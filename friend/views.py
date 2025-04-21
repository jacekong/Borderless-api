from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser

from django.http.response import JsonResponse

from .models import FriendList, FriendRequest
from .serializers import FriendListSerializer, FriendRequestSerializer
from users.models import CustomUser

from notification.models import Notification
from django.utils.translation import gettext as _

class SendFriendRequest(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # get sender user
        sender = request.user
        # get receiver id
        receiver_id = request.data.get('receiver')
        # get receiver user info
        receiver = get_object_or_404(CustomUser, user_id=receiver_id)
        
        try:
            # Check if a friend request already exists or if the users are already friends
            existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).first()
            existing_friend = FriendList.objects.filter(user=sender, friends=receiver).exists()
        except FriendList.DoesNotExist:
            existing_friend = False
        
        if existing_friend:
            return Response({'error': _('You are already friends!')}, status=status.HTTP_400_BAD_REQUEST)

        if existing_request:
            return Response({'error': _('Friend request already sent.')}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the sender and receiver are the same user
        if sender.id == receiver.id:
            return Response({'error': _('Cannot send request to yourself!')}, status=status.HTTP_400_BAD_REQUEST)
        
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        success_msg = _('Friend request send successfully.')
        # create notification
        Notification.objects.create(
            user=receiver,
            sender=sender,
            message=_(f"sent you a friend request."),
            type='friend_request'
        )
        
        return Response({'message': success_msg}, status=status.HTTP_201_CREATED)


class AcceptFriendRequest(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        receiver = request.user
        sender_id = request.data.get('sender')
        sender = get_object_or_404(CustomUser, user_id=sender_id)

        # Retrieve the friend request
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
        
        try:
            receiver_friend_list = FriendList.objects.get(user=receiver)
        except FriendList.DoesNotExist:
            receiver_friend_list = FriendList.objects.create(user=receiver)
            
        try: 
            sender_friend_list = FriendList.objects.get(user=sender)
        except FriendList.DoesNotExist:
            sender_friend_list = FriendList.objects.create(user=sender)
        
        existing_friend = FriendList.objects.filter(user=sender, friends=receiver).exists()
        if existing_friend:
            return Response({'error': _('You are already friends!')}, status=status.HTTP_400_BAD_REQUEST)
        # Check if the friend request is already accepted
        if not friend_request:
            return Response({'error': _('Friend request not found.')}, status=status.HTTP_404_NOT_FOUND)
        
        friend_request.accept()

        # notify the sender
        Notification.objects.create(
            user=sender,
            sender=receiver,
            message=_(f"accepted your friend request."),
            type='friend_request'
        )
        
        return Response({'message': _('Friend request accepted successfully.')}, status=status.HTTP_200_OK)

class DeclineFriendRequest(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        receiver = request.user
        sender_id = request.data.get('sender_id')
        sender = get_object_or_404(CustomUser, user_id=sender_id)
        
        friend_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).first()
        if not friend_request:
            return Response({'error': _('Friend request not found.')}, status=status.HTTP_404_NOT_FOUND)
        
        friend_request.decline()
        
        return Response({'message': _('Friend request declined successfully.')}, status=status.HTTP_200_OK)

# cancel the request   
class CancelFriendRequest(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        receiver = get_object_or_404(CustomUser, user_id=receiver_id)
        
        friend_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).first()
        if not friend_request:
            return Response({'error': _('Friend request not found.')}, status=status.HTTP_404_NOT_FOUND)
        
        friend_request.cancel()
        
        return Response({'message': _('Friend request cancelled successfully.')}, status=status.HTTP_200_OK)

class RemoveFriend(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        friend_id = request.data.get('friend_id')
        friend = get_object_or_404(CustomUser, user_id=friend_id)
        
        user_friend_list = FriendList.objects.get(user=user)
        user_friend_list.remove_friend(friend)
        
        return Response({'message': _('Friend removed successfully.')}, status=status.HTTP_200_OK)
    
    
# get current user friend list
class UserFriendsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        try:
            friend_list = FriendList.objects.get(user=user)
            serializer = FriendListSerializer(friend_list, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FriendList.DoesNotExist:
            return Response({'error': _('Friend list not found')}, status=status.HTTP_404_NOT_FOUND)
        
class UserFriendsRequestList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        try:
            friend_list = FriendRequest.objects.filter(receiver=user, is_active=True)
            serializer = FriendRequestSerializer(friend_list, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({'error': _('No friends request yet')} ,status=status.HTTP_404_NOT_FOUND)
        
# web
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from api.models import Post
from django.db.models import Q
from django.template.loader import render_to_string

class WebSendFriendRequest(LoginRequiredMixin, View):
    
    def post(self, request, user_id, *args, **kwargs):
        # get sender user
        sender = request.user
        # get receiver id
        receiver_id = user_id
        # get receiver user info
        receiver = get_object_or_404(CustomUser, user_id=receiver_id)
        
        try:
            # Check if a friend request already exists or if the users are already friends
            existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).first()
            existing_friend = FriendList.objects.filter(user=sender, friends=receiver).exists()
        except FriendList.DoesNotExist:
            existing_friend = False
        already_msg = _('You are already friends with')
        if existing_friend:
            Notification.objects.create(
                user=sender,
                message=f"{already_msg} {receiver.username}!",
                type='info'
            )
            return JsonResponse({'error': _('You are already friends!')})
        sent_msg = _('Friend request already sent to')
        if existing_request:
            Notification.objects.create(
                user=sender,
                message=f"{sent_msg} {receiver.username}!",
                type='info'
            )
            return JsonResponse({'error': _('Friend request already sent.')})
        
        # check if the sender and receiver are the same user
        if sender.id == receiver.id:
            Notification.objects.create(
                user=sender,
                message=_(f"Cannot send request to yourself!"),
                type='info'
            )
            return JsonResponse({'error': _('Cannot send request to yourself!')})
        
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        
        # notify sender
        Notification.objects.create(
            user=sender,
            message=_(f"Friend request sent to {receiver.username} successfully."),
            type='success'
        )
        
        # create notification
        Notification.objects.create(
            user=receiver,
            sender=sender,
            message=_(f"sent you a friend request."),
            type='friend_request'
        )
        
        return JsonResponse({'message': _('Friend request send successfully.')})
    
class WebFriendList(LoginRequiredMixin, View):
    template = 'friends/friend_list.html'
    def get(self, request, *args, **kwargs):
        user = request.user
        
        try:
            friend_list = FriendList.objects.get(user=user)
            
            friends = friend_list.friends.all()
            
            context = {
                'friend_list': friends
            }
        except FriendList.DoesNotExist:
            context = {}
            
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('partials/_friends_list.html', context)
            
            return JsonResponse({
                'html': html
            }, status=status.HTTP_200_OK)
        
        return render(request, self.template, context=context)
    
class WebFriendDetail(LoginRequiredMixin, View):
    template = 'friends/friend_detail.html'
    def get(self, request, post_author, *args, **kwargs):
        try:
            user = CustomUser.objects.get(user_id=post_author)
            current_user = request.user
            friend_id = []
            # Check if the viewer is a friend of the author
            try:
                friend_list = FriendList.objects.get(user=user)
                
                friends = friend_list.friends.all()
                friend_ids = list(friends.values_list('id', flat=True)) 
                # exludes login user
                friend_id.extend(friend_ids)
            except FriendList.DoesNotExist:
                friends = CustomUser.objects.none()
            
            # check if the user is request user
            if user == current_user:
                posts = Post.objects.prefetch_related('post_images').filter(author=user).order_by('-created_date')
            # check if request user (viewer) is a friend of the user request user  is visiting
            elif current_user in friends:
                posts = Post.objects.prefetch_related('post_images').filter(author=user).order_by('-created_date')
            # otherwise only show public posts (not friend)
            else:
                posts = Post.objects.prefetch_related('post_images').filter(author=user, is_public=True).order_by('-created_date')

            context = {'user_detail': user, 'posts': posts, 'friends': friend_id}
        except CustomUser.DoesNotExist:
            context = {'error': _('User does not exist')}

        return render(request, self.template, context=context)
    
class WebAcceptFriendRequest(LoginRequiredMixin, View):
    
    def post(self, request, user_id, *args, **kwargs):
        receiver = request.user
        sender = get_object_or_404(CustomUser, user_id=user_id)
        
        # Retrieve the friend request
        try:
            friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
        except FriendRequest.DoesNotExist:
            return JsonResponse({'error': _('Friend request has expired')}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            receiver_friend_list = FriendList.objects.get(user=receiver)
        except FriendList.DoesNotExist:
            receiver_friend_list = FriendList.objects.create(user=receiver)
            
        try: 
            sender_friend_list = FriendList.objects.get(user=sender)
        except FriendList.DoesNotExist:
            sender_friend_list = FriendList.objects.create(user=sender)
        
        existing_friend = FriendList.objects.filter(user=sender, friends=receiver).exists()
        if existing_friend:
            return JsonResponse({'error': _('You are already friends!')}, status=status.HTTP_400_BAD_REQUEST)
        # Check if the friend request is already accepted
        if not friend_request:
            return JsonResponse({'error': _('Friend request not found.')}, status=status.HTTP_404_NOT_FOUND)
        
        friend_request.accept()

        # notify the sender
        Notification.objects.create(
            user=sender,
            sender=receiver,
            message=_(f"accepted your friend request."),
            type='friend_request'
        )
        
        return JsonResponse({'success': _('Friend request accepted successfully.')}, status=status.HTTP_200_OK)