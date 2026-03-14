from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    FOLDER_CHOICES = [
        ('inbox', 'Inbox'),
        ('sent', 'Sent'),
        ('archive', 'Archive'),
        ('trash', 'Trash'),
    ]

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    folder = models.CharField(
        max_length=20,
        choices=FOLDER_CHOICES,
        default='inbox'
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject} ({self.sender} -> {self.receiver})'