from django.db import models

# Create your models here.

class Message(models.Model): 
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

# Create a Notification model to store notifications, linking it to the User and Message models.

class Notification(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message.message
