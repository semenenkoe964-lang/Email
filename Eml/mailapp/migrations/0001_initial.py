from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=120)),
                ('recipient', models.CharField(max_length=120)),
                ('subject', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('folder', models.CharField(choices=[('inbox', 'Входящие'), ('sent', 'Исходящие'), ('archive', 'Архив'), ('trash', 'Корзина')], default='inbox', max_length=20)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
