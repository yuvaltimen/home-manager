import datetime
from pyluach.dates import HebrewDate
from pyluach import parshios

from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import GroceryItem, Reminder


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


########################
#       VIEWS
########################

def home(req):
    return redirect(to=today)


def today(req):
    ctx = get_date_time_ctx()
    return render(req, 'app/today.html', ctx)


@login_required
def shopping_list(req):
    ctx = {
        'shopping_items': GroceryItem.objects.order_by('is_checked', 'name')
    }
    return render(req, 'app/shopping_list.html', ctx)


class GroceryItemListView(LoginRequiredMixin, ListView):
    model = GroceryItem
    template_name = 'app/shopping_list.html'
    context_object_name = 'shopping_items'
    ordering = ['is_checked', 'name']


class GroceryItemDetailView(LoginRequiredMixin, DetailView):
    model = GroceryItem


class GroceryItemCreateView(LoginRequiredMixin, CreateView):
    model = GroceryItem
    fields = ['name',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class GroceryItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GroceryItem
    fields = ['name',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.author


class GroceryItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GroceryItem
    success_url = '/'

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.author


@login_required
def reminders(req):
    ctx = {
        'reminders': Reminder.objects.all()
    }
    return render(req, 'app/reminders.html', ctx)
