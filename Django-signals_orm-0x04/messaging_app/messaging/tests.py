from django.test import TestCase

# Create messaging tests here.

from .models import Message

class MessageTestCase(TestCase):
    def setUp(self):
        Message.objects.create(sender='test_sender', receiver='test_receiver', message='test_message')

    def test_message(self):
        message = Message.objects.get(sender='test_sender')
        self.assertEqual(message.receiver, 'test_receiver')
        self.assertEqual(message.message, 'test_message')
