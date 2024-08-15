from django.db import models
from django.contrib.auth.models import User
from recurrence.fields import RecurrenceField


class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.author}"


class Reminder(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    schedule = RecurrenceField()
    last_modified = models.DateTimeField(auto_now=True)
