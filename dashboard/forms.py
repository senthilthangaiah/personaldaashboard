from django import forms
from .models import Task, CalendarEvent, Reminder

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'date', 'description']

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'due_date', 'completed']
