from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import GroceryItem, Reminder
from .helper_functions import get_date_time_ctx


def home(req):
    return redirect(to=today)


def today(req):
    ctx = get_date_time_ctx()
    return render(req, 'app/today.html', ctx)


class GroceryItemListView(LoginRequiredMixin, ListView):
    model = GroceryItem
    ordering = ['name', ]
    paginate_by = 50


class UserGroceryItemListView(LoginRequiredMixin, ListView):
    model = GroceryItem
    template_name = 'app/user_groceryitem_list.html'
    ordering = ['name', ]
    paginate_by = 50

    def get_queryset(self):
        usr = get_object_or_404(User, username=self.kwargs.get('username'))
        return GroceryItem.objects.filter(author=usr).order_by('name')


class GroceryItemDetailView(LoginRequiredMixin, DetailView):
    model = GroceryItem


class GroceryItemCreateView(LoginRequiredMixin, CreateView):
    model = GroceryItem
    fields = ['name', ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class GroceryItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GroceryItem
    fields = ['name', ]

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


