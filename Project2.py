#!/usr/bin/env python3
"""Project2.py — beginner-friendly weather script for OpenWeatherMap

This script is interactive: it prompts for city and API key (if not set in env).
"""
import os
import requests
from typing import Any, Dict

API_KEY_ENV = "OPENWEATHER_API_KEY"


def fetch_weather(city: str, api_key: str) -> Dict[str, Any]:
    """Call OpenWeatherMap and return parsed JSON on success.

    Raises requests.HTTPError for HTTP errors and requests.RequestException for network errors.
    """
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def pretty_print(data: Dict[str, Any]) -> None:
    """Print a small human-friendly weather report."""
    name = data.get("name", "Unknown")
    main = data.get("main", {})
    weather = (data.get("weather") or [{}])[0]
    wind = data.get("wind", {})

    print(f"\nWeather report for: {name}")
    print(f"Temperature: {main.get('temp', 'N/A')} °C")
    print(f"Feels like: {main.get('feels_like', 'N/A')} °C")
    print(f"Condition: {weather.get('description', 'N/A')}")
    print(f"Humidity: {main.get('humidity', 'N/A')} %")
    print(f"Wind speed: {wind.get('speed', 'N/A')} m/s\n")


def main() -> None:
    # Ask user for a city (interactive — no argparse required)
    city = input("Enter city name (example: Chennai): ").strip()
    if not city:
        print("City name cannot be empty. Please run again.")
        return

    # Read API key from environment; if not set, prompt the user
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        api_key = input("Enter your OpenWeatherMap API key: ").strip()
        if not api_key:
            print("API key is required. Please run again.")
            return

    try:
        data = fetch_weather(city, api_key)
        pretty_print(data)
        print("Thanks for using Surya's Weather App!")
    except requests.HTTPError as e:
        print("Failed to fetch weather:", e)
        try:
            # Try to print a helpful API error message if present
            message = e.response.json().get("message")
            if message:
                print("API says:", message)
        except Exception:
            pass
    except requests.RequestException as e:
        print("Network error:", e)


if __name__ == "__main__":
    main()
