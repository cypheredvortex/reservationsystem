# messaging/models.py
from django.db import models
from django.conf import settings
from maison.models import Maison

class Message(models.Model):
    sender     = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages',   on_delete=models.CASCADE)
    receiver   = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    maison     = models.ForeignKey(Maison, related_name='messages',                          on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent     = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.sender} → {self.receiver} @ {self.maison}"