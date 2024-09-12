from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField
import random
import numpy as np

from allauth.socialaccount.models import SocialAccount

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self._create_user(email, username, password, **extra_fields)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self._create_user(email, username, password, **extra_fields)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150,)
    user_id = models.CharField(max_length=15, unique=True)
    avatar = ResizedImageField(upload_to='avatars/', size=[320, None], null=True, blank=True, default='avatars/avatar.jpg')
    bio = models.CharField(max_length=250, blank=True, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def _get_random_id(self):
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        low_char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'x', 'y', 'z']
        capital_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'X', 'Y', 'Z']
        # initialize an empty list to store genereated ids
        id_list = []

        # returns random charactor
        lower = random.choices(low_char, weights=None, cum_weights=None, k=3)
        capital = random.choices(capital_char, weights=None, cum_weights=None, k=3)
        number = random.choices(numbers, weights=None, cum_weights=None, k=3)
        
        # append into the list
        id_list.append(lower)
        id_list.append(capital)
        id_list.append(number)
        
        # make it a 1d array
        id_list = np.array(id_list)
        id_list = id_list.flatten()
        
        # shuffle the list
        random.shuffle(id_list)
        user_id = ''
        
        for i in id_list:
            user_id += i
        
        # Check if the ID is unique
        while CustomUser.objects.filter(user_id=user_id).exists():
            lower = ''.join(random.choices(low_char, k=3))
            capital = ''.join(random.choices(capital_char, k=3))
            number = ''.join(map(str, random.choices(numbers, k=3)))
            user_id = f'{lower}{capital}{number}'

        return user_id
    
    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self._get_random_id()
        if not self.avatar:
            self.avatar = 'avatars/avatar.jpg'
        super().save(*args, **kwargs)





