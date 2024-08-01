from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True)
    amount = serializers.IntegerField(required=False, default=0)  # Adjust based on need

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'amount')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            amount=validated_data.get('amount', 0),  # Default value if not provided
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user
