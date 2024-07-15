from datetime import date

from django.core.exceptions import ValidationError
from rest_framework import serializers

from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("title", "description", "due_date")

    def validate(self, attrs):
        due_date = attrs.get("due_date")

        if due_date < date.today():
            raise serializers.ValidationError(
                {"due_date": "Date must be today or in the future."}
            )
        return attrs
