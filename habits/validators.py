from rest_framework.serializers import ValidationError


class RewardOrRelatedHabitValidator:
    """
    Проверяет, что не заполнено одновременно вознаграждение и связанная привычка,
    а также что для полезной привычки выбрано хотя бы одно из двух.
    """

    def __init__(self, reward_field, related_field, is_pleasant_field):
        """Принимает строковые названия полей из модели Django."""
        self.reward_field = reward_field
        self.related_field = related_field
        self.is_pleasant_field = is_pleasant_field

    def __call__(self, value):
        """Проверяет логику взаимоисключения наград для полезной привычки."""
        reward = value.get(self.reward_field)
        related = value.get(self.related_field)
        is_pleasant = value.get(self.is_pleasant_field, False)

        if reward and related:
            raise ValidationError(
                "Нельзя одновременно выбрать связанную привычку и указать вознаграждение."
            )

        if not is_pleasant and not reward and not related:
            raise ValidationError(
                "Для полезной привычки необходимо указать вознаграждение или связанную привычку."
            )


class EstimatedTimeValidator:
    """Проверяет, что время выполнения привычки не превышает установленный лимит."""

    def __init__(self, estimated_time_field):
        """Принимает название поля, в котором хранится время выполнения в секундах."""
        self.estimated_time_field = estimated_time_field

    def __call__(self, value):
        """Достает время выполнения и проверяет, что оно не больше 120 секунд."""
        estimated_time = value.get(self.estimated_time_field)

        if estimated_time and estimated_time > 120:
            raise ValidationError("Время выполнения должно быть не больше 120 секунд.")


class RelatedHabitIsPleasantValidator:
    """Проверяет, что связанная привычка действительно является приятной."""

    def __init__(self, related_field):
        """Принимает название поля связанной привычки."""
        self.related_field = related_field

    def __call__(self, value):
        """Проверяет флаг приятной привычки у связанного объекта."""
        related_habit_obj = value.get(self.related_field)

        if related_habit_obj and not related_habit_obj.is_pleasant:
            raise ValidationError(
                "В связанные привычки могут попадать только привычки с признаком приятной привычки."
            )


class PleasantHabitNoRewardValidator:
    """Проверяет, что у приятной привычки нет вознаграждения или связанной привычки."""

    def __init__(self, reward_field, related_field, is_pleasant_field):
        """Сохраняем имена полей для последующей проверки."""
        self.reward_field = reward_field
        self.related_field = related_field
        self.is_pleasant_field = is_pleasant_field

    def __call__(self, value):
        """Проверяет, что для приятной привычки поля наград остались пустыми."""
        reward = value.get(self.reward_field)
        related = value.get(self.related_field)
        is_pleasant = value.get(self.is_pleasant_field, False)

        if is_pleasant and (reward or related):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )


class PeriodicityValidator:
    """Проверяет, что привычка выполняется не реже чем раз в 7 дней."""

    def __init__(self, periodicity_field):
        """Принимает название поля периодичности."""
        self.periodicity_field = periodicity_field

    def __call__(self, value):
        """Проверяет, что периодичность выполнения в днях не превышает неделю."""
        periodicity = value.get(self.periodicity_field)

        if periodicity and periodicity > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
