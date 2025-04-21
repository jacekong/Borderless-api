from django.shortcuts import get_object_or_404
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
    
    def get_chat_history(self, sender, receiver):
        # Get text messages
        chat_message_sent = Messages.objects.filter(sender=sender, receiver=receiver)
        chat_message_receive = Messages.objects.filter(sender=receiver, receiver=sender)
        
        # Combine all messages into a single queryset
        chat_history = chat_message_sent.union(chat_message_receive).order_by('timestamp')
        
        return chat_history
    
    def get(self, request, *args, **kwargs):
        sender = request.user
        receiver_id = kwargs.get('user_id')
        receiver = get_object_or_404(CustomUser, user_id=receiver_id)
        
        chat_history = self.get_chat_history(sender, receiver)
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
        
        # Get chat history for all chat list entries
        chat_lists = ChatList.objects.filter(user1=logged_in_user)
        chat_list_serializer = ChatListSerializer(chat_lists, many=True, context={'request': request})
        
        chat_history_data = []
        chat_history_view = GetChatHistoryAPIView()
        
        for chat in chat_lists:
            other_user = chat.user2 
            chat_history = chat_history_view.get_chat_history(logged_in_user, other_user)
            chat_history_serializer = MessageSerializer(chat_history, many=True, context={'request': request})
            chat_history_data.append({
                'chat_list': ChatListSerializer(chat, context={'request': request}).data,
                'chat_history': chat_history_serializer.data
            })
        
        return Response({
            'chat_lists': chat_list_serializer.data,
            'chat_histories': chat_history_data
        }, status=status.HTTP_200_OK)
    
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



# web
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import JsonResponse

class ChatHistoryWeb(LoginRequiredMixin, View):
    
    def get_chat_history(self, sender, receiver):
        # Get text messages
        chat_message_sent = Messages.objects.filter(sender=sender, receiver=receiver)
        chat_message_receive = Messages.objects.filter(sender=receiver, receiver=sender)
        
        # Combine all messages into a single queryset
        chat_history = chat_message_sent.union(chat_message_receive).order_by('-timestamp')
        
        return chat_history
    
    def get(self, request, *args, **kwargs):
        sender = request.user
        receiver_id = kwargs.get('user_id')
        receiver = get_object_or_404(CustomUser, user_id=receiver_id)
        
        chat_history = self.get_chat_history(sender, receiver)
        
        context = {
            'sender': sender,
            'receiver': receiver,
            'chat_history': chat_history,
        }
        
        return render(request, '', context=context)

class ChatWebPage(LoginRequiredMixin, View):
    
    partial_template = 'chat/partials/_chat_list_partials.html'
    template = 'chat/chatlist.html'
    
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        
        # Get all chat list entries for the logged-in user
        chat_lists = ChatList.objects.filter(user1=logged_in_user)
        
        # Prepare a list to hold each contact along with their latest message
        contact_latest_messages = []
        chat_history_view = ChatHistoryWeb()
        
        for chat in chat_lists:
            other_user = chat.user2
            chat_history = chat_history_view.get_chat_history(logged_in_user, other_user)
            
            # Get the latest message (if any) from the chat history
            latest_message = chat_history.first() if chat_history.exists() else None
            
            contact_latest_messages.append({
                'contact': other_user,
                'latest_message': latest_message
            })
        
        context = {
            'chat_list': chat_lists,
            'contact_latest_messages': contact_latest_messages
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(self.partial_template, context)
            
            return JsonResponse({'html': html}, status=status.HTTP_200_OK)
        
        return render(request, self.template, context=context)
    
class ChatAreaWebView(LoginRequiredMixin, View):
    template_name = 'chat/chat_area.html'
    full_chat_area = 'chat/chat_area_full.html'
    
    def get(self, request, user_id, *args, **kwargs):
        login_user = request.user

        chat_user = CustomUser.objects.get(user_id=user_id)

        chat_history_view = ChatHistoryWeb()
        chat_history = chat_history_view.get_chat_history(login_user, chat_user)
        
        context = {
            'chat_history': chat_history,
            'chat_user': chat_user
        }
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, context)
            
            return JsonResponse({'html': html}, status=status.HTTP_200_OK)
    
        return render(request, self.full_chat_area, context=context)