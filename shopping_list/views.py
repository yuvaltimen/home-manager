from django.shortcuts import render
from .models import GroceryItem


def home(req):
    ctx = {
        'title': 'Shopping List',
        'shopping_items': GroceryItem.objects.all()
    }
    return render(req, 'shopping_list/home.html', ctx)


def about(req):
    return render(req, 'shopping_list/about.html')




