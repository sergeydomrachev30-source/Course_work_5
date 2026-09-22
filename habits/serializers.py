from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    EstimatedTimeValidator,
    PeriodicityValidator,
    PleasantHabitNoRewardValidator,
    RelatedHabitIsPleasantValidator,
    RewardOrRelatedHabitValidator,
)


class HabitsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели привычки с полной валидацией бизнес-логики."""

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RewardOrRelatedHabitValidator(
                reward_field="reward",
                related_field="related_habit",
                is_pleasant_field="is_pleasant",
            ),
            EstimatedTimeValidator(
                estimated_time_field="estimated_time",
            ),
            RelatedHabitIsPleasantValidator(
                related_field="related_habit",
            ),
            PleasantHabitNoRewardValidator(
                reward_field="reward",
                related_field="related_habit",
                is_pleasant_field="is_pleasant",
            ),
            PeriodicityValidator(
                periodicity_field="periodicity",
            ),
        ]
