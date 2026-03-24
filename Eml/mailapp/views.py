from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import mailapp.models


def get_current_user(request):
    return request.session.get('current_user', 'student@example.com')


def home(request):
    current_user = get_current_user(request)
    inbox_count = mailapp.models.Email.objects.filter(recipient=current_user, folder='inbox').count()
    sent_count = mailapp.models.Email.objects.filter(sender=current_user, folder='sent').count()
    archive_count = mailapp.models.Email.objects.filter(folder='archive').filter(recipient=current_user).count()
    trash_count = mailapp.models.Email.objects.filter(folder='trash').filter(recipient=current_user).count()

    context = {
        'current_user': current_user,
        'inbox_count': inbox_count,
        'sent_count': sent_count,
        'archive_count': archive_count,
        'trash_count': trash_count,
    }
    return render(request, 'mailapp/home.html', context)


def set_user(request):
    if request.method == 'POST':
        current_user = request.POST.get('current_user', '').strip()
        request.session['current_user'] = current_user
        messages.success(request, 'Текущий пользователь сохранён.')
    return redirect('home')


def compose_email(request):
    current_user = get_current_user(request)

    #Отправляем письмо
    if request.method == 'POST':
        recipient = request.POST.get('recipient', '').strip()
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()

        #Исходящее письмо
        mailapp.models.Email.objects.create(
            sender=current_user,
            recipient=recipient,
            subject=subject,
            body=body,
            folder='sent',
            is_read=True,
        )

        #Входящее письмо
        mailapp.models.Email.objects.create(
            sender=current_user,
            recipient=recipient,
            subject=subject,
            body=body,
            folder='inbox',
            is_read=False,
        )

        messages.success(request, 'Письмо отправлено.')
        return redirect('email_list', folder_name='sent')

    return render(request, 'mailapp/compose.html', {'current_user': current_user})


def email_list(request, folder_name):
    current_user = get_current_user(request)

    if folder_name == 'sent':
        emails = mailapp.models.Email.objects.filter(sender=current_user, folder='sent').order_by('-created_at')
    else:
        emails = mailapp.models.Email.objects.filter(recipient=current_user, folder=folder_name).order_by('-created_at')

    context = {
        'emails': emails,
        'folder_name': folder_name,
        'current_user': current_user,
    }
    return render(request, 'mailapp/email_list.html', context)


def email_detail(request, email_id):
    current_user = get_current_user(request)
    email = get_object_or_404(mailapp.models.Email, id=email_id)

    if email.recipient == current_user and not email.is_read:
        email.is_read = True
        email.save()

    return render(request, 'mailapp/email_detail.html', {'email': email, 'current_user': current_user})


def move_email(request, email_id):
    email = get_object_or_404(mailapp.models.Email, id=email_id)
    new_folder = request.POST.get('folder')

    if new_folder in ['inbox', 'archive', 'trash', 'sent']:
        email.folder = new_folder
        email.save()
        messages.success(request, 'Письмо перемещено.')
    else:
        messages.error(request, 'Неизвестная папка.')

    return redirect('email_detail', email_id=email.id)


def delete_email(request, email_id):
    email = get_object_or_404(mailapp.models.Email, id=email_id)
    email.delete()
    messages.success(request, 'Письмо удалено.')
    return redirect('home')
