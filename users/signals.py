import requests
import os
from pathlib import Path

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.base import ContentFile

from users.models import CustomUser

from allauth.socialaccount.signals import social_account_updated, social_account_added

@receiver(post_save, sender=CustomUser)
def send_msg_to_new_user(sender, instance, created, **kwargs):
    if created:
        # Check if a superuser exists
        try:
            superuser = CustomUser.objects.filter(is_superuser=True).first()
            if superuser:
                # Send a welcome message from the superuser
                send_mail(
                    '歡迎你成為Borderless的一員',
                    f'Hello {instance.username},\n\nWelcome to Borderless! If you have any questions, feel free to ask.\n\nBest regards,\n{superuser.username.capitalize()}',
                    superuser.email,
                    [instance.email],
                    fail_silently=False,
                )
        except Exception as e:
            print(f"Error sending welcome email: {e}")
            
@receiver([social_account_updated, social_account_added])
def update_user_profile(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    extra_data = sociallogin.account.extra_data

    # Extract the avatar and name from Google data
    google_avatar = extra_data.get('picture', None)
    google_name = extra_data.get('name', None)
    
    PATH = Path(__file__).resolve().parent.parent
    
    AVATARS_DIR = os.path.join(PATH, 'media', 'avatars')
    
    if not os.path.exists(AVATARS_DIR):
        os.makedirs(AVATARS_DIR)
        
    avatar_filename = f"{user.user_id}.jpg"
    avatar_filepath = os.path.join(AVATARS_DIR, avatar_filename)
    
    # Check if avatar file already exists locally
    if not os.path.isfile(avatar_filepath) and google_avatar:
        # Download the image from Google
        response = requests.get(google_avatar)
        if response.status_code == 200:
            # Save the image to the local avatars folder
            with open(avatar_filepath, 'wb') as avatar_file:
                avatar_file.write(response.content)

            # Update the user's avatar field with the local file path
            user.avatar.save(avatar_filename, ContentFile(response.content), save=True)
    
    # If the avatar was saved already, we don't need to download again
    if google_name:
        user.username = google_name
    
    user.save()