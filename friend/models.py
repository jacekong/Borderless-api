from django.db import models
from django.conf import settings

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends', related_query_name='friend')
    
    def __str__(self) -> str:
        return self.user.username
    
    def add_friend(self, account):
        '''
        add friend
        '''
        if not account in self.friends.all():
            self.friends.add(account)
            
    def remove_friend(self, account):
        '''
        remove friend
        '''
        if account in self.friends.all():
            self.friends.remove(account)
            
    def unfriend(self, removee):
        '''
        unfriend
        '''
        remover_friends_list = self
        
        remover_friends_list.remove_friend(removee)
        
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)
        
    def is_mutal_friend(self, friend):
        '''
        check if they are mutual friend
        '''
        if friend in self.friends.all():
            return True
        return False
    

class FriendRequest(models.Model):
    '''
    A friend rquest consists of two main parts:
        1. Sender:
            - Person sending/initiating the friend request
        2. Receiver:
            - Person receiving the friend request
    '''
    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(default=True, blank=True, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.sender.username
    
    def accept(self):
        '''
        Accept a friend request 
        Update both Sender and Receiver friend list
        '''
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()
                
    def decline(self):
        '''
        Decline a friend request.
        It is 'Declined' by setting the 'is_active' field to False
        '''
        self.is_active = False
        self.save()
        
    def cancel(self):
        '''
        Cancel a friend request
        It is cancelled by setting the 'is_active' field to False
        This is only different with respect to 'declining' through the notification that is generated.
        '''
        self.is_active = False
        self.save()