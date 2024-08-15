from django.db import models
from django.contrib.auth.models import User


class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.author}"
