# Generated by Django 5.1 on 2024-08-15 23:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appl', '0004_reminders_last_modified'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reminders',
            new_name='Reminder',
        ),
    ]
