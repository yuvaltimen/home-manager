import datetime

import pytz
from pyluach.dates import HebrewDate
from pyluach import parshios

from django.shortcuts import render
from .models import GroceryItem


def get_date_time_ctx():
    dt = datetime.datetime.now()
    hebrew_dt = HebrewDate.from_pydate(dt)
    parsha = parshios.getparsha_string(hebrew_dt)
    ctx = {
        'dt': dt,
        'hebrew_dt': hebrew_dt,
        'parsha': parsha,
        'ivrit_day': hebrew_dt.hebrew_date_string()
    }
    return ctx


def home(req):
    ctx = get_date_time_ctx()
    ctx.update({
        'title': 'Shopping List',
        'shopping_items': GroceryItem.objects.order_by('is_checked', 'name')
    })
    return render(req, 'shopping_list/home.html', ctx)


def about(req):
    ctx = get_date_time_ctx()
    return render(req, 'shopping_list/about.html', ctx)




