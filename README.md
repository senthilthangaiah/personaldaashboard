# Daily Dashboard with AI Agents

This project is a Django-based web application that serves as a daily dashboard, integrating AI agents to provide a summary of tasks, events, and reminders. It also fetches real-time data such as weather forecasts, stock market updates, and news articles from various categories.

## Features
- **Task Management:** Create, update, and delete tasks.
- **Calendar Events:** Manage calendar events with descriptions and dates.
- **Reminders:** Set reminders with due dates and mark them as completed.
- **AI Summarization:** Summarize tasks, events, and reminders using an AI agent.
- **Weather Forecast:** Get real-time weather updates for a specified city.
- **Stock Market Data:** Fetch the latest data for Sensex and Nifty.
- **News Aggregator:** Fetch and summarize news articles from various categories.

## Installation

### Prerequisites
- Python 3.8 or higher
- Django 3.2 or higher
- pip (Python package installer)

### Steps to Install and Run the Project

#### Clone the Repository
```bash
git clone https://github.com/yourusername/daily-dashboard.git
cd daily-dashboard
```

#### Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Set Up Environment Variables
Create a `.env` file in the root directory and add the following variables:
```
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
```

#### Apply Migrations
```bash
python manage.py migrate
```

#### Run the Development Server
```bash
python manage.py runserver
```

#### Access the Dashboard
Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the dashboard.

## Project Structure
```
dashboard/
  ├── models.py       # Defines the database models for tasks, calendar events, and reminders.
  ├── views.py        # Contains the logic for handling requests and rendering templates.
  ├── urls.py         # Defines the URL patterns for the application.
  ├── templates/dashboard/  # Contains the HTML templates for the dashboard.
  ├── utils.py        # Contains utility functions, such as text summarization.
requirements.txt       # Lists the project dependencies.
```

## Usage
- **Dashboard:** The main page (`/`) displays a summary of tasks, events, reminders, weather, and stock market data.
- **News:** The news page (`/news`) displays categorized news articles.
- **Tasks:** Manage tasks through the tasks page (`/tasks`).
- **Calendar:** Manage calendar events through the calendar page (`/calendar`).
- **Reminders:** Manage reminders through the reminders page (`/reminders`).

## Snapshots
![Dashboard View](https://github.com/senthilthangaiah/personaldaashboard/blob/master/images/img1.png)
![News]([image2.jpeg](https://github.com/senthilthangaiah/personaldaashboard/blob/master/images/img2.png)
![Task]([image1.jpeg](https://github.com/senthilthangaiah/personaldaashboard/blob/master/images/img3.png)
![Calendar]([image2.jpeg](https://github.com/senthilthangaiah/personaldaashboard/blob/master/images/img4.png)
![Reminder](https://github.com/senthilthangaiah/personaldaashboard/blob/master/images/img1.png)

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Django for the web framework.
- OpenWeatherMap for weather data.
- Alpha Vantage for stock market data.
- DuckDuckGo for news aggregation.

## Contact
For any questions or feedback, please open an issue on GitHub or contact the repository owner.

