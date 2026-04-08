# 🌐 Live Weather & News Dashboard

A beautiful real-time dashboard built with Python (Flask) showing live weather and Indian news — built as a college project.

---

## Features

- 🌤️ Live weather with temperature, feels like, humidity, wind, pressure, visibility
- ⏱️ Upcoming 6-hour hourly forecast
- 📰 Live Indian news with 7 category tabs (General, Technology, Science, Health, Sports, Entertainment, Business)
- 🔍 City search bar
- 🔄 Auto-refreshes every 5 minutes
- 🎨 Glassmorphism dark UI

---

## Tech Stack

| Layer    | Technology                                              |
|----------|---------------------------------------------------------|
| Backend  | Python, Flask                                           |
| Weather  | [Open-Meteo API](https://open-meteo.com/) *(no key needed)* |
| News     | [NewsAPI.org](https://newsapi.org/)                     |
| Frontend | HTML, CSS, Vanilla JavaScript                           |

---

## Project Structure

```
weather-news-dashboard/
├── app.py              # Flask backend & API routes
├── .env                # API keys and config
├── requirements.txt    # Python dependencies
└── templates/
    └── index.html      # Dashboard UI
```

---

## Setup & Installation

### 1. Clone or download the project

```bash
cd weather-news-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

```env
WEATHER_API_KEY=not_required   # Open-Meteo needs no key
NEWS_API_KEY=your_newsapi_org_key_here
DEFAULT_CITY=Kolkata
```

Get your free NewsAPI key at [newsapi.org/register](https://newsapi.org/register).

### 5. Run the app

```bash
python app.py
```

Open your browser at `http://127.0.0.1:5000`

---

## API Sources

- **Weather** — [Open-Meteo](https://open-meteo.com/) — free, no API key required
- **News** — [NewsAPI.org](https://newsapi.org/) — free developer tier, 100 requests/day

---
## cd "/mnt/c/users/user/desktop/weather&news/weather-news-dashboard" && source venv/bin/activate && python app.py

## Screenshots

> Add screenshots of your dashboard here for the college submission.

---

## Author

Made with ❤️ for college project.
