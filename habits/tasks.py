from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def check_habits_and_send_reminders():
    """Фоновая задача для проверки времени привычек и отправки уведомлений."""
    now = timezone.localtime(timezone.now())
    current_date = now.date()
    current_time = now.time()

    habits = Habit.objects.filter(
        is_pleasant=False,
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        user__telegram_chat_id__isnull=False,
    )

    for habit in habits:
        if (
            habit.last_reminder_date is None
            or (current_date - habit.last_reminder_date).days >= habit.periodicity
        ):
            message = f"Напоминание! Я буду {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}."

            send_telegram_message(habit.user.telegram_chat_id, message)

            habit.last_reminder_date = current_date
            habit.save()
