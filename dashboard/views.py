from django.utils import timezone
import requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, CalendarEvent, Reminder
from .forms import TaskForm, CalendarEventForm, ReminderForm
from .utils import summarize_text
from duckduckgo_search import DDGS
from datetime import datetime
import yfinance as yf

def dash_summary():
    # Fetch today's data
    today = datetime.now().date()
    tasks = Task.objects.filter(completed=False)
    events = CalendarEvent.objects.filter(date__date=today)
    reminders = Reminder.objects.filter( completed=False)
    #reminders = Reminder.objects.filter(due_date__date=today, completed=False)

    # Format data for summarization
    text_to_summarize = "Tasks:\n"
    text_to_summarize += "\n".join([f"- {task.title}: {task.description}" for task in tasks])
    text_to_summarize += "\n\nEvents:\n"
    text_to_summarize += "\n".join([f"- {event.title}: {event.description}" for event in events])
    text_to_summarize += "\n\nReminders:\n"
    text_to_summarize += "\n".join([f"- {reminder.title} (Due: {reminder.due_date})" for reminder in reminders])
    
    text_to_summarize += '\n Above are my Tasks, Events, Reminders. Just summarize it by each category and give Highlights'

    # Generate summary
    print('### suummary ', text_to_summarize)
    text_to_summarize.replace('\n', '<br>')
    summary = summarize_text(text_to_summarize)
    return summary

# Replace with your actual API keys
OPENWEATHERMAP_API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXX'


def get_weather_forecast(city="Chennai"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
        }
        return weather
    return None



def get_stock_data():
    # Fetch Sensex (^BSESN) and Nifty (^NSEI) data
    sensex = yf.Ticker("^BSESN")
    nifty = yf.Ticker("^NSEI")

    # Get the latest data
    sensex_data = sensex.history(period="1d")
    nifty_data = nifty.history(period="1d")
    print('### snx ',sensex_data['High'])

    if not sensex_data.empty and not nifty_data.empty:
        sensex_info = {
            'symbol': 'Sensex',
            'last_price': sensex_data['Close'].iloc[-1],
            'open': sensex_data['Open'].iloc[-1],
            'high': sensex_data['High'].iloc[-1],
            'low': sensex_data['Low'].iloc[-1],
            'volume': sensex_data['Volume'].iloc[-1],
        }
        nifty_info = {
            'symbol': 'Nifty',
            'last_price': nifty_data['Close'].iloc[-1],
            'open': nifty_data['Open'].iloc[-1],
            'high': nifty_data['High'].iloc[-1],
            'low': nifty_data['Low'].iloc[-1],
            'volume': nifty_data['Volume'].iloc[-1],
        }
        return {'sensex': sensex_info, 'nifty': nifty_info}
    return None
    
def index(request):
    # Fetch news, events, reminders, and tasks as before
    categories = {
        "Tamil Nadu Politics": "Tamil Nadu politics news in Tamil",
        "Technology": "latest technology news",
        "Startup and Entrepreneurship": "startup and entrepreneurship news",
        "India News": "India news from The Morning Context",
        "World Wide Tech News": "worldwide technology news from The Morning Context",
    }

    ddgs = DDGS()
    categorized_news = {}

    for category, query in categories.items():
        news_results = ddgs.news(keywords=query, region="wt-wt", max_results=2)
        summarized_articles = []
        for item in news_results:
            summary = item.get('body', '')
            summarized_articles.append({
                'title': item.get('title', 'No title'),
                'summary': summary,
                'url': item.get('url', '#'),
            })
        categorized_news[category] = summarized_articles

    upcoming_events = CalendarEvent.objects.filter(
        date__gte=timezone.now(),
        date__lte=timezone.now() + timezone.timedelta(days=7)
    )

    incomplete_reminders = Reminder.objects.filter(completed=False)
    pending_tasks = Task.objects.filter(completed=False)
    my_summary = dash_summary()

    # Fetch weather and stock data
    weather = get_weather_forecast()
    sensex = get_stock_data()

    context = {
        'categorized_news': categorized_news,
        'upcoming_events': upcoming_events,
        'incomplete_reminders': incomplete_reminders,
        'pending_tasks': pending_tasks,
        'summary': my_summary,
        'weather': weather,
        'sensex': sensex,
    }
    return render(request, 'dashboard/index.html', context)
    
    
def news(request):
    # Define categories and their search queries
    categories = {
        "Tamil Nadu Politics": "Tamil Nadu politics news in Tamil",
        "Technology": "latest technology news",
        "Startup and Entrepreneurship": "startup and entrepreneurship news",
        "India News": "India news from The Morning Context",
        "World Wide ": "worldwide important and Trend news ",
    }

    # Fetch news for each category
    ddgs = DDGS()
    news_data = {}
    for category, query in categories.items():
        news_results = ddgs.news(keywords=query, region="wt-wt", max_results=5)  # Fetch top 5 news articles per category
        
        # Summarize each news article
        summarized_news = []
        for news_item in news_results:
            #summary = summarize_text(news_item.get('body', ''))  # Summarize the news body
            summary = news_item.get('body', '')
            summarized_news.append({
                'title': news_item.get('title', 'No title'),
                'body': summary,  # Use the summarized text
                'source': news_item.get('source', 'Unknown'),
                'url': news_item.get('url', '#'),
            })
        
        news_data[category] = summarized_news
    weather = get_weather_forecast()
    # Pass the news data to the template
    context = {
        'initial_news': news_data,
        'weather': weather,
    }
    return render(request, 'dashboard/news.html', context)    
    
# Task Views
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm()
    return render(request, 'dashboard/task_form.html', {'form': form})

def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'dashboard/task_form.html', {'form': form})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    return render(request, 'dashboard/confirm_delete.html', {'object': task})


def tasks(request):
    tasks = Task.objects.all()
    weather = get_weather_forecast()
    return render(request, 'dashboard/tasks.html', {'tasks': tasks, 'weather': weather})

def calendar(request):
    events = CalendarEvent.objects.all()
    weather = get_weather_forecast()
    return render(request, 'dashboard/calendar.html', {'events': events, 'weather': weather})

def reminders(request):
    reminders = Reminder.objects.all()
    weather = get_weather_forecast()
    return render(request, 'dashboard/reminders.html', {'reminders': reminders, 'weather': weather})

def create_calendar_event(request):
    if request.method == 'POST':
        form = CalendarEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = CalendarEventForm()
    weather = get_weather_forecast()
    return render(request, 'dashboard/calendar_event_form.html', {'form': form, 'weather': weather})

def update_calendar_event(request, event_id):
    event = get_object_or_404(CalendarEvent, id=event_id)
    if request.method == 'POST':
        form = CalendarEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = CalendarEventForm(instance=event)
    weather = get_weather_forecast()
    return render(request, 'dashboard/calendar_event_form.html', {'form': form, 'weather': weather })

def delete_calendar_event(request, event_id):
    event = get_object_or_404(CalendarEvent, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('calendar')
    weather = get_weather_forecast()        
    return render(request, 'dashboard/confirm_delete.html', {'object': event, 'weather': weather})

def create_reminder(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reminders')
    else:
        form = ReminderForm()
    weather = get_weather_forecast()
    return render(request, 'dashboard/reminder_form.html', {'form': form, 'weather': weather})

def update_reminder(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('reminders')
    else:
        form = ReminderForm(instance=reminder)
    weather = get_weather_forecast()
    return render(request, 'dashboard/reminder_form.html', {'form': form, 'weather': weather })

def delete_reminder(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id)
    if request.method == 'POST':
        reminder.delete()
        return redirect('reminders')
    weather = get_weather_forecast()
    return render(request, 'dashboard/confirm_delete.html', {'object': reminder, 'weather': weather })
