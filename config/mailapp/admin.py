from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sender',
        'receiver',
        'subject',
        'folder',
        'is_read',
        'created_at'
    )
    list_filter = ('folder', 'is_read', 'created_at')
    search_fields = ('subject', 'body', 'sender__username', 'receiver__username')