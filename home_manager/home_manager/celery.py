import os
from celery import Celery

# from webpush import send_user_notification
# from appl.models import User, Reminder
# from appl.helper_functions import next_occurrence_in_timeframe
# from datetime import datetime, timedelta


app = Celery('yummy_celery', broker=os.environ.get('CELERY_BROKER'), backend=os.environ.get('CELERY_BACKEND'))


# @app.task
# def send_push(usrname, head, body):
#     payload = {"head": head, "body": body}
#     usr = User.objects.filter(username=usrname).first()
#     if not usr:
#         return
#     print(f"Sending push to {usrname}!")
#     send_user_notification(usr, payload=payload, ttl=100)


@app.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y
#
#
# @task()
# def schedule_next_reminder(usrname, reminder_id):
#     usr = User.objects.filter(username=usrname).first()
#     if not usr:
#         print(f"No such user {usrname}")
#         return
#
#     reminder = Reminder.objects.filter(id=reminder_id).first()
#     if not reminder:
#         print(f"No such reminder {reminder_id}")
#         return
#
#     rn = datetime.now()
#     yesterday = rn + timedelta(days=-1)  # Need to start 1 day ago bc `next_occurrence_in_timeframe` is non-inclusive
#     futr = rn + timedelta(weeks=104)  # scan for 2 years
#     next_occ = next_occurrence_in_timeframe(reminder.schedule, yesterday, futr)
#     if not next_occ:
#         print(f"No occurrences until {futr}, delaying til then")
#         schedule_next_reminder(usrname, reminder_id, _schedule=futr)
#         return
#
#     time_to_send = reminder.time_to_send
#     dt = datetime(next_occ.year, next_occ.month, next_occ.day, time_to_send.hour, time_to_send.minute)
#
#     # Since `recurrence` only deals with dates and not datetimes, we need to manually
#     # check if we're about to schedule an already-past occurrence. Check this by
#     # comparing the now to the constructred dt.
#     # Only send the push message if we haven't passed the dt yet
#     if rn < dt:
#         print(f"Sending push to {usrname} at {dt.strftime('%I:%M%p %b %d, %Y')}!")
#         send_push(usrname, head=reminder.name, body=reminder.description, _schedule=dt)
#
#     # Regardless if we passed the dt, schedule the next reminder to be sent
#     next_occ_after_that = next_occurrence_in_timeframe(reminder.schedule, rn, futr)
#     dt_next_occurrence = datetime(next_occ_after_that.year, next_occ_after_that.month, next_occ_after_that.day,
#                                   time_to_send.hour, time_to_send.minute) - timedelta(minutes=10)
#     schedule_next_reminder(usrname, reminder_id, _schedule=dt_next_occurrence)
