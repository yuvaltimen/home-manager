from django import forms
from .models import Reminder


class ReminderUpdateForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ('name', 'description', 'schedule')
