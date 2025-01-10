from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingAppTests(TestCase):
    def setUp(self):
        # Create test users
        self.sender = User.objects.create_user(username="sender", password="password")
        self.receiver = User.objects.create_user(username="receiver", password="password")

    def test_message_creation(self):
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is a test message."
        )

        # Check if the message is saved correctly
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.content, "Hello, this is a test message.")

    def test_notification_creation(self):
        # Create a message, which should trigger the notification signal
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is another test message."
        )

        # Check if a notification is created for the receiver
        notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notifications.count(), 1)

        notification = notifications.first()
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)  # Default value should be False

    def test_no_notification_for_sender(self):
        # Create a message
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Yet another test message."
        )

        # Check that the sender has no notifications
        notifications = Notification.objects.filter(user=self.sender)
        self.assertEqual(notifications.count(), 0)
