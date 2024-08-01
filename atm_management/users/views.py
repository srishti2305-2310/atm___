from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from .models import CustomUser
from .serializers import UserSerializer
from .utils import generate_access_token, generate_refresh_token, decode_token

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    username_or_email = request.data.get('username')
    password = request.data.get('password')

    if not username_or_email or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    user_data = UserSerializer(user).data
    return Response({'access': access_token, 'refresh': refresh_token, 'data': user_data}, status=status.HTTP_200_OK)

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        payload = decode_token(refresh_token)
        if isinstance(payload, dict) and 'error' in payload:
            return Response({'error': payload['error']}, status=status.HTTP_401_UNAUTHORIZED)

        if not payload:
            return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = CustomUser.objects.get(id=payload['user_id'])
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        new_access_token = generate_access_token(user)
        return Response({'access': new_access_token}, status=status.HTTP_200_OK)
