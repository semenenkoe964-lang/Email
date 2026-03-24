from django.db import models


class Email(models.Model):
    FOLDER_CHOICES = [
        ('inbox', 'Входящие'),
        ('sent', 'Исходящие'),
        ('archive', 'Архив'),
        ('trash', 'Корзина'),
    ]

    sender = models.CharField(max_length=120)
    recipient = models.CharField(max_length=120)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    folder = models.CharField(max_length=20, choices=FOLDER_CHOICES, default='inbox')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject} ({self.sender} -> {self.recipient})'
