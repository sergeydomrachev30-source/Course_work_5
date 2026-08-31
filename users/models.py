from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User, где уникальным идентификатором
    для авторизации является email вместо username.
    """

    def create_user(self, email, password, **extra_fields):
        """Создает и сохраняет пользователя с указанным email и паролем."""
        if not email:
            raise ValueError("Email должен быть указан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Создает и сохраняет суперпользователя с указанным email и паролем."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя, использующая email вместо username."""

    username = None
    objects = UserManager()
    email = models.EmailField(unique=True, verbose_name="Email")
    telegram_chat_id = models.BigIntegerField(
        blank=True, null=True, verbose_name="ID чата Telegram"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Возвращает строковое представление пользователя в виде его email."""
        return self.email
