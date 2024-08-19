from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .forms import ReminderUpdateForm
from .models import GroceryItem, Reminder
from .helper_functions import get_date_time_ctx


##################
#   HOME
##################
def home(req):
    return redirect(to=today)


##################
#   TODAY
##################
def today(req):
    print(req.device)
    ctx = get_date_time_ctx()
    if req.device['is_mobile']:
        return render(req, 'app/today.html', ctx)
    else:
        return render(req, 'app/today.html', ctx)


##################
#   SHOPPING_LIST
##################
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

    def get_success_url(self):
        submit_type = self.request.POST.get('submit_type')
        print(submit_type)
        if submit_type == 'submit_and_add':
            return reverse('app_groceryitem_create')
        return reverse('app_groceryitem_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class GroceryItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GroceryItem
    fields = ['name', ]

    def get_success_url(self):
        return reverse('app_groceryitem_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.author


class GroceryItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GroceryItem

    def get_success_url(self):
        return reverse('app_groceryitem_list')

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.author


##################
#   REMINDER
##################
class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    paginate_by = 50


class UserReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = 'app/user_reminder_list.html'
    paginate_by = 50

    def get_queryset(self):
        usr = get_object_or_404(User, username=self.kwargs.get('username'))
        return Reminder.objects.filter(author=usr).order_by('name')


class ReminderDetailView(LoginRequiredMixin, DetailView):
    model = Reminder


class ReminderCreateView(LoginRequiredMixin, CreateView):
    model = Reminder
    form_class = ReminderUpdateForm

    def get_success_url(self):
        submit_type = self.request.POST.get('submit_type')
        print(submit_type)
        if submit_type == 'submit_and_add':
            return reverse('app_reminder_create')
        return reverse('app_reminder_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReminderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reminder
    form_class = ReminderUpdateForm

    def get_success_url(self):
        submit_type = self.request.POST.get('submit_type')
        print(submit_type)
        if submit_type == 'submit_and_add':
            return reverse('app_reminder_create')
        return reverse('app_reminder_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.author


class ReminderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reminder

    def get_success_url(self):
        return reverse('app_reminder_list')

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.author


