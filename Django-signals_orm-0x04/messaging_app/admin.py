from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp', 'is_read')
    search_fields = ('user__email', 'message__message_body')
    list_filter = ('is_read', 'timestamp')