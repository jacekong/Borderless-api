import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from chat.models import AudioMessage, Messages
from users.models import CustomUser
import uuid
from io import BytesIO
from django.conf import settings
from django.urls import reverse
from urllib.parse import urljoin

class ChatConsumer(AsyncWebsocketConsumer):
    # connect websocket
    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            chat_with_user = self.scope['url_route']['kwargs']['user_id']
            user_ids = [user.user_id, chat_with_user]
            user_ids = sorted([str(user.user_id), str(chat_with_user)])
            self.room_group_name = f'chat_{user_ids[0]}-{user_ids[1]}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    # disconnect websocket
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # receive messages from websocket
    async def receive(self,text_data=None, bytes_data=None):
        data  = json.loads(text_data)
        message_type = data.get('message_type')
        if message_type == 'text':
            await self.handle_text_message(data)
        elif message_type == 'audio':
            await self.handle_audio_message(data)
        elif message_type == 'image':
            await self.handle_image_message(data)
    
    # text mesage handler
    async def handle_text_message(self, data):
        message = data.get('message')
        sender = data.get('sender')
        receiver = self.scope['url_route']['kwargs']['user_id']
        timestamp = data.get('timestamp')
        
        await self.save_message(sender, receiver, message)
        # send message to channel group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': message,
                'sender': sender,
                'timestamp': timestamp,
                'message_type': 'text'
            }
        )
    
    # voice message handler
    async def handle_audio_message(self, data):
        sender = data.get('sender')
        receiver = self.scope['url_route']['kwargs']['user_id']
        audio_data = data.get('audio')
        duration = data.get('duration')
        timestamp = data.get('timestamp')
        
        audio_message = await self.save_audio_message(sender, receiver, audio_data, duration)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'audio_message',
                'audio': str(settings.BASE_URL + audio_message),
                'sender': sender,
                'duration': duration,
                'timestamp': timestamp,
                'message_type': 'audio'
            }
        )
        
    # images message handler 
    async def handle_image_message(self, event):
        sender = event['sender']
        image = event['images']
        message_type = event['message_type']
        timestamp = event['timestamp']
        
        # Send the image message to the WebSocket client
        await self.send(text_data=json.dumps({
            'sender': sender,
            'images': image,
            'timestamp': timestamp,
            'message_type': message_type,
        }))
    
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']
        message_type = event['message_type']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp,
            'message_type': message_type
        }))
        
    async def audio_message(self, event):
        audio = event['audio']
        sender = event['sender']
        timestamp = event['timestamp']
        message_type = event['message_type']
        duration = event['duration']
        
        await self.send(text_data=json.dumps({
            'audio': audio,
            'sender': sender,
            'duration': duration,
            'timestamp': timestamp,
            'message_type': message_type
        }))
        
    @sync_to_async
    def save_message(self, sender, receiver, message):
        sender = CustomUser.objects.get(user_id=sender)
        receiver = CustomUser.objects.get(user_id=receiver)
        
        Messages.objects.create(sender=sender, receiver=receiver, message=message)
        
    @sync_to_async
    def save_audio_message(self, sender, receiver, audio_data, duration):
        sender = CustomUser.objects.get(user_id=sender)
        receiver = CustomUser.objects.get(user_id=receiver)
        
        # Generate a unique filename
        unique_filename = str(uuid.uuid4()) + '.wav'
        
        audio_bytes = bytes(audio_data)
        
        # Convert bytes data to a file-like object
        audio_file = BytesIO(audio_bytes)
        
        audio_message = AudioMessage(sender=sender, receiver=receiver, duration=duration)
        audio_message.audio_file.save(unique_filename, audio_file, duration)
        audio_message.save()
        
        # Construct the URL of the saved audio file
        audio_file_path = audio_message.audio_file.name
        audio_url = urljoin(settings.MEDIA_URL, audio_file_path)
        
        return audio_url
    
# notifications
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            # Add user to the appropriate group to receive notifications
            await self.channel_layer.group_add(
                "notifications", 
                self.channel_name
            )
            
            await self.accept()

    async def disconnect(self, close_code):
        # Remove user from notification group
        await self.channel_layer.group_discard(
            "notifications", 
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('message_type')
        if message_type == 'text':
            self.send_text_notification(data)
        elif message_type == 'image':
            self.send_image_notification(data)
        elif message_type == 'audio':
            self.send_audio_notification(data)
    
    # event handlers
    async def send_text_notification(self, event):
        login_user = self.scope['user']
        login_user = login_user.user_id
        
        timestamp = event['timestamp']
        
        receiver = event['receiver']
        sender = event['sender']
        
        sender_id = event['sender_id']
        print(sender_id)
        
        text = event['notification']
        avatar = event['avatar']
        
        if receiver == login_user:
            await self.send(text_data=json.dumps({
                'notification': text,
                'receiver': receiver,
                'sender': sender,
                'sender_id': sender_id,
                'avatar': str(settings.BASE_URL + avatar),
                'timestamp': timestamp,
                'message_type': 'text',
            }))
            
    async def send_image_notification(self, event):
        login_user = self.scope['user']
        login_user = login_user.user_id
        
        timestamp = event['timestamp']
        
        receiver = event['receiver']
        sender = event['sender']
        
        sender_id = event['sender_id']

        image = event['notification']
        avatar = event['avatar']
        
        if receiver == login_user:
            await self.send(text_data=json.dumps({
                    'notification': str(settings.BASE_URL + image),
                    'receiver': receiver,
                    'sender': sender,
                    'sender_id': sender_id,
                    'avatar': str(settings.BASE_URL + avatar),
                    'timestamp': timestamp,
                    'message_type': 'image',
                }))
            
    async def send_audio_notification(self, event):
        login_user = self.scope['user']
        login_user = login_user.user_id
        
        timestamp = event['timestamp']
        
        receiver = event['receiver']
        sender = event['sender']
        
        sender_id = event['sender_id']

        audio = event['notification']
        avatar = event['avatar']
        
        if receiver == login_user:
            await self.send(text_data=json.dumps({
                    'notification': audio,
                    'receiver': receiver,
                    'sender': sender,
                    'sender_id': sender_id,
                    'avatar': str(settings.BASE_URL + avatar),
                    'timestamp': timestamp,
                    'message_type': 'audio',
                }))
        

            

        
        
        
    

        
        
    

