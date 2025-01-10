from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Logs the old content of a message into the MessageHistory model before it is updated.
    """
    if instance.pk:  # Check if the message already exists (is being updated)
        # Fetch the existing message from the database
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            # Create a history record if the content has changed
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            # Mark the message as edited
            instance.edited = True
