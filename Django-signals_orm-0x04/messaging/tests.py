from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

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

class MessageEditLoggingTests(TestCase):
    def setUp(self):
        # Create test users
        self.sender = User.objects.create_user(username="sender", password="password")
        self.receiver = User.objects.create_user(username="receiver", password="password")
        # Create an initial message
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original message content"
        )

    def test_message_edit_logs_history(self):
        # Update the message content
        self.message.content = "Updated message content"
        self.message.save()

        # Check if a history record is created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)

        # Verify the history record contains the old content
        history_record = history.first()
        self.assertEqual(history_record.old_content, "Original message content")

    def test_multiple_edits_log_multiple_histories(self):
        # First edit
        self.message.content = "First edit"
        self.message.save()

        # Second edit
        self.message.content = "Second edit"
        self.message.save()

        # Check if two history records are created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 2)

        # Verify the history records
        self.assertEqual(history[0].old_content, "Original message content")
        self.assertEqual(history[1].old_content, "First edit")

    def test_edited_flag_set_on_edit(self):
        # Update the message content
        self.message.content = "Edited content"
        self.message.save()

        # Reload the message and check the edited flag
        self.message.refresh_from_db()
        self.assertTrue(self.message.edited)

    def test_no_history_on_no_content_change(self):
        # Save the message without changing the content
        self.message.save()

        # Check that no history record is created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 0)