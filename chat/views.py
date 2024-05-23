from rest_framework.permissions import IsAuthenticated, AllowAny
from chat.consumers import ChatConsumer
from users.models import CustomUser
from .models import AudioMessage, ChatList, ImageMessage, MessageNotification, Messages
from .serializers import AudioMessageSerializer, ChatListSerializer, ImageMessageSerializer, MessageSerializer, NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view, permission_classes

# get user's text chat history
class GetChatHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        sender = request.user

        receiver = kwargs.get('user_id')
        receiver = CustomUser.objects.get(user_id=receiver)
        
        # get text messages
        chat_message_sent = Messages.objects.filter(sender=sender, receiver=receiver)
        chat_message_receive = Messages.objects.filter(sender=receiver, receiver=sender)
        
        
        chat_history = chat_message_sent.union(chat_message_receive)
        # Combine all messages into a single queryset
        
        # Sort the chat history by timestamp
        # chat_history.sort(key=lambda x: x.timestamp)
        
        serializer = MessageSerializer(chat_history, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ImageMessageHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        sender = request.user
        
        receiver = kwargs.get('user_id')
        receiver = CustomUser.objects.get(user_id=receiver)
        
        # get image messages
        image_messages_sent = ImageMessage.objects.filter(sender=sender, receiver=receiver)
        image_messages_receive = ImageMessage.objects.filter(sender=receiver, receiver=sender)
        
        chat_history = image_messages_sent.union(image_messages_receive)
        
        # chat_history.sort(key=lambda x: x.timestamp)
        
        serializer = ImageMessageSerializer(chat_history, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# when user start to chat the chat list record will be created
class ChatListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        data = request.data
        user1_id = data.get('user1_id')
        user2_id = data.get('user2_id')
        
        # Check if both user IDs are provided
        if not user1_id or not user2_id:
            return Response({'error': 'Both user IDs are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if both users exist
        try:
            user1 = CustomUser.objects.get(user_id=user1_id)
            user2 = CustomUser.objects.get(user_id=user2_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'One or both users do not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new chat list entry
        ChatList.objects.create(user1=user1, user2=user2)
        # serializer = ChatListSerializer(chat_list)
        return Response(status=status.HTTP_201_CREATED)
    
class ChatListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user

        chat_lists = ChatList.objects.filter(user1=logged_in_user)
        serializer = ChatListSerializer(chat_lists, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ImageMessageCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        sender = request.user
        receiver = request.data.get('receiver')
        image_file = request.data.get('images')
        
        receiver = CustomUser.objects.get(user_id=receiver)
        
        image_message = ImageMessage.objects.create(sender=sender, receiver=receiver, images=image_file)
        
        image_url = request.build_absolute_uri(image_message.images.url)
        
        serializer = ImageMessageSerializer(image_message, context={'request': request})
        
        # response_data = serializer.data
        data = serializer.data
        
        user_ids = [sender.user_id, receiver.user_id]
        user_ids = sorted([str(sender.user_id), str(receiver.user_id)])
        room_group_name = f'chat_{user_ids[0]}-{user_ids[1]}'
        
        # Notify channel consumers about the new image
        channel_layer = get_channel_layer()

        # send image messages
        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'handle_image_message', # handler must matche the handler in consumers.py
                'sender': sender.user_id,
                'images': image_url,
                'timestamp': data['timestamp'],
                'message_type': 'image',
            }
        )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# audio chat history
class AudioChatHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        sender = request.user
        
        receiver = kwargs.get('user_id')
        receiver = CustomUser.objects.get(user_id=receiver)
        
        # get audio messages
        audio_messages_sent = AudioMessage.objects.filter(sender=sender, receiver=receiver)
        audio_messages_receive = AudioMessage.objects.filter(sender=receiver, receiver=sender)
        
        chat_history = audio_messages_sent.union(audio_messages_receive)
        
        # chat_history.sort(key=lambda x: x.timestamp)
        
        serializer = AudioMessageSerializer(chat_history, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_notification(request):
    
    noti = MessageNotification.objects.all()
    
    serilizaer =  NotificationSerializer(noti, many=True)
    
    return Response(serilizaer.data, status=status.HTTP_200_OK)
    
        
        
    
        
        

