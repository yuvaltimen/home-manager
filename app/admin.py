from django.contrib import admin
from .models import GroceryItem, Reminder

admin.site.register(GroceryItem)
admin.site.register(Reminder)
