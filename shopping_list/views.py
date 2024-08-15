import datetime
from pyluach.dates import HebrewDate
from pyluach import parshios

from django.shortcuts import render
from .models import GroceryItem

dt = datetime.datetime.now()
hebrew_dt = HebrewDate.from_pydate(dt)
parsha = parshios.getparsha_string(hebrew_dt)
ctx = {
    'dt': dt,
    'hebrew_dt': hebrew_dt,
    'parsha': parsha,
    'ivrit_day': hebrew_dt.hebrew_date_string()
}

def home(req):
    ctx.update({
        'title': 'Shopping List',
        'shopping_items': GroceryItem.objects.order_by('is_checked', 'name')
    })
    return render(req, 'shopping_list/home.html', ctx)


def about(req):
    dt = datetime.datetime.now()
    hebrew_dt = HebrewDate.from_pydate(dt)
    parsha = parshios.getparsha_string(hebrew_dt)
    ctx = {
        'dt': dt,
        'hebrew_dt': hebrew_dt,
        'parsha': parsha,
        'ivrit_day': hebrew_dt.hebrew_date_string()
    }
    return render(req, 'shopping_list/about.html', ctx)




