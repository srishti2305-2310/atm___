from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import CustomUser
import utils as utl

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        payload = utl.decode_token(token)

        if isinstance(payload, dict) and 'error' in payload:
            raise AuthenticationFailed(payload['error'])

        if not payload:
            raise AuthenticationFailed('Invalid or expired token')

        try:
            user = CustomUser.objects.get(id=payload['user_id'])
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, None)
