from django.conf import settings
from django.db import models


class Habit(models.Model):
    """Модель привычки, созданной пользователем."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель привычки",
        blank=True,
        null=True,
    )
    place = models.CharField(max_length=255, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие (сама привычка)")

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связанная приятная привычка",
    )

    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    periodicity = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность (в днях)"
    )
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Вознаграждение"
    )
    estimated_time = models.PositiveIntegerField(
        default=60, verbose_name="Время на выполнение (в секундах)"
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")
    last_reminder_date = models.DateField(
        blank=True, null=True, verbose_name="Дата последнего напоминания"
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        """Возвращает текстовое описание привычки."""
        return f"{self.action} в {self.time} ({self.place})"
