from django import forms
from appl.models import Reminder


class ReminderUpdateForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ('name', 'description', 'time_to_send', 'schedule')
        widgets = {
            'time_to_send': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }


class GroceryItemDeleteManyForm(forms.Form):
    item_ids = forms.CharField(widget=forms.HiddenInput())
