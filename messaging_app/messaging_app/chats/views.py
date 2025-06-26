from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Message.objects.filter(conversation__participants=self.request.user)
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise PermissionError("You are not a participant of this conversation.")
        serializer.save(sender=self.request.user)
