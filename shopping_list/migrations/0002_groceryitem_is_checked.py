# Generated by Django 5.1 on 2024-08-15 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groceryitem',
            name='is_checked',
            field=models.BooleanField(default=False),
        ),
    ]
