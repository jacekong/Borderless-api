from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from users.models import CustomUser

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

