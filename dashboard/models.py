from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.title

class Reminder(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
