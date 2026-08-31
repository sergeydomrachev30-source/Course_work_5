from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""

    password = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User
        fields = ("email", "password", "telegram_chat_id")

    def create(self, validated_data):
        """Создает пользователя, используя встроенный метод создания с хэшированием пароля."""
        user = User.objects.create_user(**validated_data)
        return user
