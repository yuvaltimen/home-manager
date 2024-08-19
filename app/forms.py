from django import forms
from .models import Reminder


class ReminderUpdateForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ('name', 'description', 'time_to_send', 'schedule')
        widgets = {
            'time_to_send': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }
