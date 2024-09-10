from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from django.views.generic.edit import DeletionMixin
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from appl.forms import ReminderUpdateForm
from appl.models import GroceryItem, Reminder
from appl.helper_functions import get_date_time_ctx


##################
#   HOME
##################
def home(req):
    return redirect(to=today)


##################
#   TODAY
##################
@never_cache
def today(req):
    ctx = get_date_time_ctx()
    return render(req, 'appl/today.html', ctx)


##################
#   SHOPPING_LIST
##################
class GroceryItemListView(LoginRequiredMixin, ListView):
    model = GroceryItem
    ordering = ['name', ]

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserGroceryItemListView(LoginRequiredMixin, ListView):
    model = GroceryItem
    template_name = 'appl/user_groceryitem_list.html'
    ordering = ['name', ]

    def get_queryset(self):
        usr = get_object_or_404(User, username=self.kwargs.get('username'))
        # send_push.delay(self.kwargs.get('username'), head="Hello", body="Hello world!", countdown=10)
        return GroceryItem.objects.filter(author=usr).order_by('name')

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class GroceryItemDetailView(LoginRequiredMixin, DetailView):
    model = GroceryItem

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class GroceryItemCreateView(LoginRequiredMixin, CreateView):
    model = GroceryItem
    fields = ['name', ]

    def get_success_url(self):
        submit_type = self.request.POST.get('submit_type')
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


class GroceryItemDeleteAllView(LoginRequiredMixin, DeletionMixin, View):
    model = GroceryItem

    def post(self, request, *args, **kwargs):
        deleted_count, _ = GroceryItem.objects.all().delete()
        messages.success(request, f"Deleted {deleted_count} items successfully.")
        # Redirect to the appropriate page after deletion
        return redirect('app_groceryitem_list')

    def get_success_url(self):
        return reverse('app_groceryitem_list')


class GroceryItemConfirmDeleteAllView(LoginRequiredMixin, View):
    model = GroceryItem

    def post(self, req):
        return render(req, 'appl/groceryitem_confirm_delete_all.html')

    def get_success_url(self):
        return reverse('app_groceryitem_list')


##################
#   REMINDER
##################
class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = 'appl/user_reminder_list.html'

    def get_queryset(self):
        usr = get_object_or_404(User, username=self.kwargs.get('username'))
        return Reminder.objects.filter(author=usr).order_by('name')

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ReminderDetailView(LoginRequiredMixin, DetailView):
    model = Reminder

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ReminderCreateView(LoginRequiredMixin, CreateView):
    model = Reminder
    form_class = ReminderUpdateForm

    def get_success_url(self):
        submit_type = self.request.POST.get('submit_type')
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

