from django import template
from itertools import zip_longest
from appl.helper_functions import next_occurrence_in_timeframe
import datetime

register = template.Library()


@register.filter(name='zip_lists')
def zip_lists(a, b):
    return zip_longest(a, b)


@register.filter(name='replace_with_space')
def replace_with_space(value, to_replace):
    return value.replace(to_replace, " ")


@register.filter(name='display_next_occurrence')
def display_next_occurrence(obj):
    time_of_day_of_reminder = obj.time_to_send
    recurrence_obj = obj.schedule
    today = datetime.datetime.now()
    two_years_in_future = today + datetime.timedelta(weeks=104)
    next_occurrence = next_occurrence_in_timeframe(recurrence_obj, today, two_years_in_future)
    if not next_occurrence:
        return "No reminders in next 2 years"
    return (f"Next reminder at "
            f"{time_of_day_of_reminder.strftime('%I:%M %p')} on "
            f"{next_occurrence.strftime('%b %d, %Y')}")
