from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone


class Message (models.Model):
    sender = models.ForeignKey(
        User, related_name='message_sender', on_delete=models.CASCADE, null=True)
    receiver = models.ForeignKey(
        User, related_name='message_receiver', on_delete=models.CASCADE,)
    subject = models.CharField(max_length=75)
    message = models.TextField(blank=True)
    isRead = models.BooleanField(default=False)
    creationDate = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.subject
