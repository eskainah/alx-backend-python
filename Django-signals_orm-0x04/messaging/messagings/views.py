
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page
from django.shortcuts import render
from .models import Message

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log out the user before deleting
        user.delete()
        return redirect('home')  # Redirect to a homepage or goodbye page

def get_threaded_messages(user):
    """
    Get top-level messages (parent_message is None) with their first-level replies prefetched.
    """
    messages = (
        Message.objects.filter(receiver=user, parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
    )
    return messages

def get_all_replies(message):
    """
    Recursively get all nested replies to a message.
    """
    replies = []
    children = message.replies.all()
    for child in children:
        replies.append(child)
        replies.extend(get_all_replies(child))
    return replies

def unread_inbox(request):
    user = request.user
    unread_msgs = Message.unread_messages.unread_for_user(user)

@cache_page(60)  # Cache this view for 60 seconds
def conversation_messages(request, conversation_id):
    # Example: Fetch messages in a conversation (adjust as needed)
    messages = Message.objects.filter(parent_message__isnull=True).select_related('sender', 'receiver').order_by('timestamp')

    return render(request, 'messages/conversation.html', {'messages': messages})
