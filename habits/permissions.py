from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Класс проверяет, что пользователь должен иметь доступ по механизму
    CRUD (создание, чтение, обновление, удаление) только к своим собственным привычкам
    """

    def has_object_permission(self, request, view, obj):
        """Метод проверяет конкретный объект (в нашем случае — привычку) и должен
        вернуть True, если доступ разрешен, или False, если запрещен."""
        return request.user == obj.user
