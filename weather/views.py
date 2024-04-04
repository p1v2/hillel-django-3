from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

from weather.mock_api import get_weather


@api_view(['GET'])
def weather(request):
    city = request.query_params.get('city')

    cached_weather = cache.get(f"weather_{city}")

    if cached_weather:
        return Response({"result": cached_weather})
    else:
        weather_result = get_weather(city)
        cache.set(f"weather_{city}", weather_result, 60)
        return Response({"result": weather_result})
