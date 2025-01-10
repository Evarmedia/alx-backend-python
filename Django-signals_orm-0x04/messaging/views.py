from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Message

# Create your views here.

def delete_user(request, user_id):
    """
    View to delete a user account and clean up related data.
    """
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect('home')  # Redirect to the home page after deletion

def get_threaded_conversation(request, message_id):
    """
    Fetch a message and all its replies recursively.
    """
    def fetch_replies(message):
        replies = message.replies.prefetch_related('sender', 'receiver')
        return [
            {
                'id': reply.id,
                'content': reply.content,
                'sender': reply.sender.username,
                'receiver': reply.receiver.username,
                'timestamp': reply.timestamp,
                'replies': fetch_replies(reply),
            }
            for reply in replies
        ]

    # Get the root message
    root_message = get_object_or_404(Message.objects.prefetch_related('replies'), id=message_id)
    
    conversation = {
        'id': root_message.id,
        'content': root_message.content,
        'sender': root_message.sender.username,
        'receiver': root_message.receiver.username,
        'timestamp': root_message.timestamp,
        'replies': fetch_replies(root_message),
    }

    return JsonResponse(conversation, safe=False)