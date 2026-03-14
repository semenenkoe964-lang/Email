from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_message, name='send_message'),
    path('inbox/<str:username>/', views.inbox_messages, name='inbox_messages'),
    path('sent/<str:username>/', views.sent_messages, name='sent_messages'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('message/<int:message_id>/move/', views.move_message, name='move_message'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
]