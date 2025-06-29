from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification
from django.contrib.auth.models import User
@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    if instance.pk:
        old = Message.objects.get(pk=instance.pk)
        if old.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=old.content
            )
            instance.edited = True
            
@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()