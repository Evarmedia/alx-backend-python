from django.db.models.signals import post_save
from django.dispatch import receiver
from chats.models import Message
from .models import Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the receiver of the message
        Notification.objects.create(
            user=instance.conversation.participants.exclude(id=instance.sender.id).first(),
            message=instance,
            content=f"You have received a new message from {instance.sender.get_full_name()}",
            timestamp=instance.sent_at
        )