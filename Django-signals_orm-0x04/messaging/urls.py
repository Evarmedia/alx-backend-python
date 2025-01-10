from django.urls import path
from .views import get_threaded_conversation

urlpatterns = [
    path('conversation/<int:message_id>/', get_threaded_conversation, name='threaded_conversation'),
]

# The /conversation/<message_id>/ endpoint retrieves a message and its replies.
