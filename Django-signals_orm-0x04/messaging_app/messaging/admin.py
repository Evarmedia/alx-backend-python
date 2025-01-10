from django.contrib import admin

# Register your models here.

from .models import Message

admin.site.register(Message)
# admin.site.register(Message) registers the Message model with the Django admin site.
