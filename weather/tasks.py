from celery import shared_task
from django.core.cache import cache

from weather.mock_api import get_weather


@shared_task
def get_weather_task():
    cities = ["Kyiv", "London"]

    for city in cities:
        weather_result = get_weather(city)
        cache.set(f"weather_{city}", weather_result, 60)

    print("Weather updated!")
