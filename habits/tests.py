from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone as django_timezone
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.services import send_telegram_message
from habits.tasks import check_habits_and_send_reminders

User = get_user_model()


class HabitCreateTestCase(APITestCase):

    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.user = User.objects.create_user(
            email="test@user.com", password="testpassword123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тест успешного создания полезной привычки через API."""
        url = reverse("habits-list")

        data = {
            "place": "Кухня",
            "time": "08:00:00",
            "action": "Выпить стакан воды",
            "periodicity": 1,
            "estimated_time": 60,
            "reward": "Съесть ягоду",
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Habit.objects.filter(action="Выпить стакан воды").exists())

    def test_reward_and_related_habit_together_fails(self):
        """Тест: одновременный выбор вознаграждения и связанной привычки должен вернуть ошибку 400."""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Ванная",
            time="21:00:00",
            action="Принять ванну с пеной",
            is_pleasant=True,
            estimated_time=60,
            periodicity=1,
        )

        data = {
            "place": "Кухня",
            "time": "08:00:00",
            "action": "Выпить стакан воды",
            "periodicity": 1,
            "estimated_time": 60,
            "reward": "Съесть ягоду",
            "related_habit": pleasant_habit.id,
        }

        response = self.client.post(reverse("habits-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TelegramIntegrationTestCase(APITestCase):
    """Тестирование интеграции с Telegram API с использованием Mock."""

    @patch("requests.post")
    def test_send_telegram_message_success(self, mock_post):
        """Проверка, что функция отправки правильно формирует запрос."""

        mock_post.return_value.status_code = 200

        send_telegram_message(1219513797, "Тест")

        mock_post.assert_called_once()


class CeleryTasksTestCase(APITestCase):
    """Тестирование периодических задач Celery."""

    @patch("habits.tasks.send_telegram_message")
    def test_check_habits_and_send_reminders(self, mock_send):
        """Проверка, что задача Celery находит привычку и вызывает отправку."""
        import datetime

        now = django_timezone.localtime(django_timezone.now())
        current_hour = now.hour
        current_minute = now.minute

        user = User.objects.create_user(
            email="celery@test.com", password="123", telegram_chat_id="1219513797"
        )

        for hour_shift in [0, -3, 3]:
            target_hour = (current_hour + hour_shift) % 24
            test_time = datetime.time(hour=target_hour, minute=current_minute)

            Habit.objects.create(
                user=user,
                place="Дом",
                time=test_time,
                action=f"Сделать зарядку {hour_shift}",
                estimated_time=60,
                periodicity=1,
                is_pleasant=False,
            )

        check_habits_and_send_reminders()

        mock_send.assert_called()
