# Generated by Django 5.1 on 2024-08-15 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_reminders'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminders',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
