# messaging/urls.py

from django.urls import path
from .views import send_message, inbox, sent_messages, conversation

urlpatterns = [
    path('maison/<int:maison_id>/message/', send_message,    name='send_message'),
    path('inbox/',               inbox,          name='inbox'),
    path('sent/',                sent_messages,  name='sent_messages'),
    path('conversation/<int:message_id>/', conversation, name='conversation'),
]