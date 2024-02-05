from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication


class HalsoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        haslo = request.GET.get('haslo')

        if haslo == 'SlavaUkraini':
            return User.objects.get(is_superuser=True), None

        return None
