from django.db.models.signals import post_save
from django.dispatch import receiver
from appl.models import Reminder
# from appl.tasks import schedule_next_reminder


# @receiver(post_save, sender=Reminder)
# def schedule_reminder_job(sender, instance, created, **kwargs):
#     schedule_next_reminder(instance.author.username, instance.id)
