import os

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from telegram.client import send_message
from rest_framework.response import Response


@api_view(['POST'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def telegram(request):
    # Telegram webhook view
    # Get telegram message
    # Echo message
    print(request.data)

    text = request.data['message']['text']
    name = request.data['message']['from'].get('first_name')

    telegram_text = f"{name}: {text}"

    send_message(192484569, telegram_text)

    # Some comment

    return Response({'status': 'OK!'})