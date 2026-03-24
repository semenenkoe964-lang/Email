from django.test import TestCase
from django.urls import reverse
import mailapp.models


class EmailTests(TestCase):
    def setUp(self):
        session = self.client.session
        session['current_user'] = 'student@example.com'
        session.save()

    def test_send_email_creates_two_records(self):
        response = self.client.post(reverse('compose_email'), {
            'recipient': 'friend@example.com',
            'subject': 'Тест',
            'body': 'Привет!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(mailapp.models.Email.objects.count(), 2)

    def test_open_email_marks_it_read(self):
        email = mailapp.models.Email.objects.create(
            sender='friend@example.com',
            recipient='student@example.com',
            subject='Письмо',
            body='Текст',
            folder='inbox',
            is_read=False,
        )
        self.client.get(reverse('email_detail', args=[email.id]))
        email.refresh_from_db()
        self.assertTrue(email.is_read)

    def test_move_email_to_archive(self):
        email = mailapp.models.Email.objects.create(
            sender='friend@example.com',
            recipient='student@example.com',
            subject='Письмо',
            body='Текст',
            folder='inbox',
            is_read=False,
        )
        self.client.post(reverse('move_email', args=[email.id]), {'folder': 'archive'})
        email.refresh_from_db()
        self.assertEqual(email.folder, 'archive')
