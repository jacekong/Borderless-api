import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from api.models import Post, PostComments
from users.models import CustomUser
import datetime
from django.utils.timezone import now

class CommentConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            comment_on_post = self.scope['url_route']['kwargs']['post_id']
            self.room_group_name = f'comment_on_{comment_on_post}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self,text_data=None, bytes_data=None):
        data  = json.loads(text_data)
        comment = data['comment']

        sender = self.scope['user'].user_id
        
        comment_sender = self.scope['user']
        
        post = self.scope['url_route']['kwargs']['post_id']
        
        await self.save_comment(sender, post, comment)
            
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'post_comment',
                'comment': comment,
                'sender': comment_sender.username,
                'sender_avatar': comment_sender.avatar.url,
                'timestamp': now().isoformat(),
            }
        )
    
    async def post_comment(self, event):
        comment = event['comment']
        sender = event['sender']
        sender_avatar = event['sender_avatar']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'comment': comment,
            'sender': sender,
            'sender_avatar': sender_avatar,
            'timestamp': timestamp,
        }))
        
    @sync_to_async
    def save_comment(self, sender, post, comment):
        sender = CustomUser.objects.get(user_id=sender)
        post = Post.objects.get(post_id=post)
        
        PostComments.objects.create(sender=sender, post=post, comment=comment)
        