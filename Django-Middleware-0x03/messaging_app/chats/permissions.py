# chats/permissions.py
from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to interact with messages in that conversation.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated for any access
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj can be a Message or Conversation instance.
        We check if the request.user is a participant.
        """
        if hasattr(obj, 'conversation'):  # obj is a Message
            return request.user in obj.conversation.participants.all()
        elif hasattr(obj, 'participants'):  # obj is a Conversation
            return request.user in obj.participants.all()
        return False
