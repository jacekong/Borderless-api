import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from api.models import Post, PostComments
from users.models import CustomUser
from django.utils.timezone import now
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from notification.models import Notification

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
        
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        comment_text = data['comment']
        parent_id = data.get('parent', None)
        sender = self.scope['user']
        post_id = self.scope['url_route']['kwargs']['post_id']

        post = await self._get_post(post_id)
        parent_comment = await self._get_parent_comment(post, parent_id)
        comment = await self.save_comment(sender.user_id, post_id, comment_text, parent_comment)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'post_comment',
                'comment': comment_text,
                'sender': sender.username,
                'avatar': str(settings.BASE_URL + sender.avatar.url),
                'timestamp': now().isoformat(),
                'parent': parent_comment.id if parent_comment else None,
                'id': comment.id if comment else None
            }
        )
    
    async def post_comment(self, event):
        await self.send(text_data=json.dumps({
            'comment': event['comment'],
            'sender': event['sender'],
            'avatar': event['avatar'],
            'timestamp': event['timestamp'],
            'parent': event['parent'],
            'id': event['id'],
        }))
        
    @database_sync_to_async
    def _get_post(self, post_id):
        return Post.objects.get(post_id=post_id)
    
    @database_sync_to_async
    def _get_parent_comment(self, post, parent_id):
        if not parent_id:
            return None
        try:
            return PostComments.objects.get(id=parent_id, post=post)
        except PostComments.DoesNotExist:
            return None
    
    @sync_to_async
    def save_comment(self, sender_id, post_id, comment_text, parent_comment=None):
        sender = CustomUser.objects.get(user_id=sender_id)
        post = Post.objects.get(post_id=post_id)
        comment = PostComments.objects.create(
            sender=sender,
            post=post,
            comment=comment_text,
            parent=parent_comment
        )
        # create notification
        # if the comment's post is not login user's post
        if post.author != sender and not parent_comment:
            Notification.objects.create(
                user=post.author,
                sender=sender,
                type='comment',
                message=f'comment on your post: {comment_text}'
            )
        return comment