from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitsPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitsSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с личными привычками текущего пользователя.
    Обеспечивает полный цикл CRUD (создание, чтение, обновление, удаление)
    с автоматической фильтрацией данных по владельцу, пагинацией и
    проверкой прав доступа.
    """

    serializer_class = HabitsSerializer
    pagination_class = HabitsPaginator

    def get_permissions(self):
        """
        Определяет права доступа в зависимости от действия (action).
        """
        if self.action in ["update", "partial_update", "destroy", "retrieve"]:
            return [IsAuthenticated(), IsOwner()]
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        """
        Возвращает список привычек, принадлежащих только текущему авторизованному пользователю.
        """
        if self.request.user.is_anonymous:
            return Habit.objects.none()
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Автоматически назначает текущего авторизованного пользователя создателем привычки.
        """
        serializer.save(user=self.request.user)


class PublicHabitListAPIView(generics.ListAPIView):
    """Класс для вывода списка публичных привычек."""

    serializer_class = HabitsSerializer
    pagination_class = HabitsPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """метод выводит только те привычки, у которых признак публичности равен True."""
        return Habit.objects.filter(is_public=True)
