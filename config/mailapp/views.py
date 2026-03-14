import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Message
from .utils import message_to_dict


@csrf_exempt
def send_message(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Разрешён только POST'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный JSON'}, status=400)

    sender_username = data.get('sender')
    receiver_username = data.get('receiver')
    subject = data.get('subject')
    body = data.get('body')

    if not sender_username or not receiver_username or not subject or not body:
        return JsonResponse({'error': 'Не все поля заполнены'}, status=400)

    sender = get_object_or_404(User, username=sender_username)
    receiver = get_object_or_404(User, username=receiver_username)

    # Письмо в папке "Отправленные" у отправителя
    sent_message = Message.objects.create(
        sender=sender,
        receiver=receiver,
        subject=subject,
        body=body,
        folder='sent',
        is_read=True
    )

    # Письмо в папке "Входящие" у получателя
    inbox_message = Message.objects.create(
        sender=sender,
        receiver=receiver,
        subject=subject,
        body=body,
        folder='inbox',
        is_read=False
    )

    return JsonResponse({
        'message': 'Письмо успешно отправлено',
        'sent_message': message_to_dict(sent_message),
        'inbox_message': message_to_dict(inbox_message),
    }, status=201)


def inbox_messages(request, username):
    if request.method != 'GET':
        return JsonResponse({'error': 'Разрешён только GET'}, status=405)

    user = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        receiver=user,
        folder='inbox'
    ).order_by('-created_at')

    data = [message_to_dict(message) for message in messages]
    return JsonResponse({'messages': data}, status=200)


def sent_messages(request, username):
    if request.method != 'GET':
        return JsonResponse({'error': 'Разрешён только GET'}, status=405)

    user = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        sender=user,
        folder='sent'
    ).order_by('-created_at')

    data = [message_to_dict(message) for message in messages]
    return JsonResponse({'messages': data}, status=200)


def message_detail(request, message_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Разрешён только GET'}, status=405)

    message = get_object_or_404(Message, id=message_id)

    if message.folder == 'inbox' and not message.is_read:
        message.is_read = True
        message.save()

    return JsonResponse(message_to_dict(message), status=200)


@csrf_exempt
def move_message(request, message_id):
    if request.method != 'PATCH':
        return JsonResponse({'error': 'Разрешён только PATCH'}, status=405)

    message = get_object_or_404(Message, id=message_id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный JSON'}, status=400)

    new_folder = data.get('folder')
    allowed_folders = ['inbox', 'sent', 'archive', 'trash']

    if new_folder not in allowed_folders:
        return JsonResponse({'error': 'Недопустимая папка'}, status=400)

    message.folder = new_folder
    message.save()

    return JsonResponse({
        'message': 'Письмо перемещено',
        'data': message_to_dict(message)
    }, status=200)


@csrf_exempt
def delete_message(request, message_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Разрешён только DELETE'}, status=405)

    message = get_object_or_404(Message, id=message_id)
    message.delete()

    return JsonResponse({'message': 'Письмо удалено'}, status=200)