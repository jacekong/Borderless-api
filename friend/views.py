from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser

from users.serializers import UserSerializer
from .models import FriendList, FriendRequest
from .serializers import FriendListSerializer, FriendRequestSerializer
from users.models import CustomUser

class SendFriendRequest(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # get sender user
        sender = request.user
        # get receiver id
        receiver_id = request.data.get('receiver')
        # get receiver user info
        receiver = get_object_or_404(CustomUser ,user_id=receiver_id)
        
        try:
            # Check if a friend request already exists or if the users are already friends
            existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).first()
            existing_friend = FriendList.objects.filter(user=sender, friends=receiver).exists()
        except FriendList.DoesNotExist:
            existing_friend = False

        if existing_friend:
            return Response({'error': 'You are already friends!'}, status=status.HTTP_400_BAD_REQUEST)

        if existing_request:
            return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the sender and receiver are the same user
        if sender.id == receiver.id:
            return Response({'error': 'Cannot send request to yourself!'}, status=status.HTTP_400_BAD_REQUEST)
        
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        
        return Response({'message': 'Friend request send successfully.'}, status=status.HTTP_201_CREATED)


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
              

        if not friend_request:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
 
        
        friend_request.accept()
    
        
        return Response({'message': 'Friend request accepted successfully.'}, status=status.HTTP_200_OK)

class DeclineFriendRequest(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        receiver = request.user
        sender_id = request.data.get('sender_id')
        sender = get_object_or_404(CustomUser, user_id=sender_id)
        
        friend_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).first()
        if not friend_request:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        friend_request.decline()
        
        return Response({'message': 'Friend request declined successfully.'}, status=status.HTTP_200_OK)

# cancel the request   
class CancelFriendRequest(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        receiver = get_object_or_404(CustomUser, user_id=receiver_id)
        
        friend_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).first()
        if not friend_request:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        friend_request.cancel()
        
        return Response({'message': 'Friend request cancelled successfully.'}, status=status.HTTP_200_OK)

class RemoveFriend(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        friend_id = request.data.get('friend_id')
        friend = get_object_or_404(CustomUser, user_id=friend_id)
        
        user_friend_list = FriendList.objects.get(user=user)
        user_friend_list.remove_friend(friend)
        
        return Response({'message': 'Friend removed successfully.'}, status=status.HTTP_200_OK)
    
    
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
            return Response({'error': 'Friend list not found'}, status=status.HTTP_404_NOT_FOUND)
        
class UserFriendsRequestList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        try:
            friend_list = FriendRequest.objects.filter(receiver=user, is_active=True)
            serializer = FriendRequestSerializer(friend_list, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'No friends request yet'} ,status=status.HTTP_404_NOT_FOUND)
        
# web
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

class WebSendFriendRequest(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        # get sender user
        sender = request.user
        # get receiver id
        receiver_id = request.data.get('receiver')
        # get receiver user info
        receiver = get_object_or_404(CustomUser ,user_id=receiver_id)
        
        try:
            # Check if a friend request already exists or if the users are already friends
            existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).first()
            existing_friend = FriendList.objects.filter(user=sender, friends=receiver).exists()
        except FriendList.DoesNotExist:
            existing_friend = False

        if existing_friend:
            return Response({'error': 'You are already friends!'}, status=status.HTTP_400_BAD_REQUEST)

        if existing_request:
            return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the sender and receiver are the same user
        if sender.id == receiver.id:
            return Response({'error': 'Cannot send request to yourself!'}, status=status.HTTP_400_BAD_REQUEST)
        
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        
        return Response({'message': 'Friend request send successfully.'}, status=status.HTTP_201_CREATED)
    
    