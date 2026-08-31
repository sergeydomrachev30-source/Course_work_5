from rest_framework.pagination import PageNumberPagination


class HabitsPaginator(PageNumberPagination):
    """Класс делит список на аккуратные порции (страницы) и показывает на одной странице ровно 5 привычек."""

    page_size = 5
