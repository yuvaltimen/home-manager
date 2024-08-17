from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from recurrence.fields import RecurrenceField


class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.author}"

    def get_absolute_url(self):
        return reverse('app_shopping_detail', kwargs={'pk': self.pk})


class Reminder(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    schedule = RecurrenceField()
    last_modified = models.DateTimeField(auto_now=True)
