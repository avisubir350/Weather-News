from flask import Flask, render_template, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Kolkata")

WEATHER_BASE = "https://api.open-meteo.com/v1"
GEO_BASE = "https://geocoding-api.open-meteo.com/v1"
NEWS_BASE = "https://newsapi.org/v2"


@app.route("/")
def index():
    return render_template("index.html", default_city=DEFAULT_CITY)


@app.route("/api/weather")
def get_weather():
    city = request.args.get("city", DEFAULT_CITY)
    try:
        # Step 1: geocode city name to lat/lon
        geo = requests.get(
            f"{GEO_BASE}/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=5,
        ).json()

        results = geo.get("results")
        if not results:
            return jsonify({"error": f"City '{city}' not found"}), 404

        loc = results[0]
        lat, lon = loc["latitude"], loc["longitude"]
        country = loc.get("country", "")
        city_name = loc.get("name", city)

        # Step 2: fetch current + hourly weather
        weather = requests.get(
            f"{WEATHER_BASE}/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,surface_pressure,visibility",
                "hourly": "temperature_2m,weather_code",
                "wind_speed_unit": "kmh",
                "forecast_days": 2,
                "timezone": "auto",
            },
            timeout=5,
        ).json()

        cur = weather["current"]
        hourly = weather["hourly"]

        # WMO weather code → description + icon emoji
        def wmo_info(code):
            mapping = {
                0: ("Clear Sky", "☀️"), 1: ("Mainly Clear", "🌤️"), 2: ("Partly Cloudy", "⛅"),
                3: ("Overcast", "☁️"), 45: ("Foggy", "🌫️"), 48: ("Icy Fog", "🌫️"),
                51: ("Light Drizzle", "🌦️"), 53: ("Drizzle", "🌦️"), 55: ("Heavy Drizzle", "🌧️"),
                61: ("Slight Rain", "🌧️"), 63: ("Rain", "🌧️"), 65: ("Heavy Rain", "🌧️"),
                71: ("Slight Snow", "🌨️"), 73: ("Snow", "❄️"), 75: ("Heavy Snow", "❄️"),
                80: ("Rain Showers", "🌦️"), 81: ("Showers", "🌧️"), 82: ("Heavy Showers", "⛈️"),
                95: ("Thunderstorm", "⛈️"), 96: ("Thunderstorm+Hail", "⛈️"), 99: ("Heavy Thunderstorm", "⛈️"),
            }
            return mapping.get(code, ("Unknown", "🌡️"))

        desc, icon_emoji = wmo_info(cur["weather_code"])

        # Next 5 hourly slots
        from datetime import datetime
        now_hour = datetime.now().hour
        forecast = []
        for i, t in enumerate(hourly["time"]):
            h = int(t[11:13])
            if h >= now_hour and len(forecast) < 6:
                d, emoji = wmo_info(hourly["weather_code"][i])
                forecast.append({
                    "time": t[11:16],
                    "temp": round(hourly["temperature_2m"][i]),
                    "icon": emoji,
                    "desc": d,
                })

        return jsonify({
            "city": city_name,
            "country": country,
            "temp": round(cur["temperature_2m"]),
            "feels_like": round(cur["apparent_temperature"]),
            "humidity": cur["relative_humidity_2m"],
            "wind": round(cur["wind_speed_10m"], 1),
            "description": desc,
            "icon": icon_emoji,
            "visibility": round(cur.get("visibility", 0) / 1000, 1),
            "pressure": cur["surface_pressure"],
            "forecast": forecast,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/news")
def get_news():
    category = request.args.get("category", "general")

    # Map category to search keywords for India-focused news
    category_queries = {
        "general": "India",
        "technology": "India technology",
        "science": "India science",
        "health": "India health",
        "sports": "India sports",
        "entertainment": "India entertainment Bollywood",
        "business": "India business economy",
    }

    try:
        # Try top-headlines with country=in first
        resp = requests.get(
            f"{NEWS_BASE}/top-headlines",
            params={
                "category": category,
                "country": "in",
                "pageSize": 12,
                "apiKey": NEWS_API_KEY,
            },
            timeout=5,
        ).json()

        articles_raw = []
        if resp.get("status") == "ok":
            articles_raw = resp.get("articles", [])

        # Fallback: use /everything with India keyword if no results
        if not articles_raw:
            query = category_queries.get(category, "India")
            resp2 = requests.get(
                f"{NEWS_BASE}/everything",
                params={
                    "q": query,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": 12,
                    "apiKey": NEWS_API_KEY,
                },
                timeout=5,
            ).json()
            if resp2.get("status") == "ok":
                articles_raw = resp2.get("articles", [])
            else:
                return jsonify({"error": resp2.get("message", "News fetch failed")}), 500

        articles = []
        for a in articles_raw:
            if a.get("title") and a["title"] != "[Removed]":
                articles.append({
                    "title": a["title"],
                    "source": a["source"]["name"],
                    "url": a["url"],
                    "image": a.get("urlToImage"),
                    "published": a.get("publishedAt", "")[:10],
                    "description": a.get("description", ""),
                })

        return jsonify({"articles": articles, "category": category})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
