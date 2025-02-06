from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news, name='news'),
    path('tasks/', views.tasks, name='tasks'),
    path('calendar/', views.calendar, name='calendar'),
    path('reminders/', views.reminders, name='reminders'),
    # Task URLs
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/update/<int:task_id>/', views.update_task, name='update_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),

    # CalendarEvent URLs
    path('calendar/create/', views.create_calendar_event, name='create_calendar_event'),
    path('calendar/update/<int:event_id>/', views.update_calendar_event, name='update_calendar_event'),
    path('calendar/delete/<int:event_id>/', views.delete_calendar_event, name='delete_calendar_event'),

    # Reminder URLs
    path('reminders/create/', views.create_reminder, name='create_reminder'),
    path('reminders/update/<int:reminder_id>/', views.update_reminder, name='update_reminder'),
    path('reminders/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),

]
