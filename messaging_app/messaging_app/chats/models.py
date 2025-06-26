
from django.db import models

class Conversation(models.Model):
    participants = models.ManyToManyField('users.CustomUser', related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} between {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    sender = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='messages_sent')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
