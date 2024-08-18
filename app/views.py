import datetime
from pytz import timezone
from skyfield.api import load
from skyfield.framelib import ecliptic_frame
from pyluach.dates import HebrewDate
from pyluach import parshios

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


def get_moon_phase(current_dt):

    ts = load.timescale()
    t = ts.from_datetime(timezone('US/Eastern').localize(current_dt))

    eph = load('de421.bsp')
    sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

    e = earth.at(t)
    s = e.observe(sun).apparent()
    m = e.observe(moon).apparent()

    _, slon, _ = s.frame_latlon(ecliptic_frame)
    _, mlon, _ = m.frame_latlon(ecliptic_frame)
    phase = (mlon.degrees - slon.degrees) % 360.0

    if phase < 0.2:
        return "New_Moon"
    elif 0.2 < phase < 89.8:
        return "Waxing_Crescent"
    elif 89.8 <= phase < 90.2:
        return "First_Quarter"
    elif 90.2 <= phase < 179.8:
        return "Waxing_Gibbous"
    elif 179.8 <= phase < 180.2:
        return "Full_Moon"
    elif 180.2 <= phase < 269.8:
        return "Waning_Gibbous"
    elif 269.8 <= phase <= 270.2:
        return "Last_Quarter"
    elif phase < 360.0:
        return "Waning_Crescent"
    else:
        return "Unknown"


def get_date_time_ctx():
    dt = datetime.datetime.now()
    moon_phase = get_moon_phase(dt)
    hebrew_dt = HebrewDate.from_pydate(dt)
    parsha = parshios.getparsha_string(hebrew_dt)
    ctx = {
        'dt': dt,
        'moon_phase': moon_phase,
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
