from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets, permissions
from rest_framework.serializers import Serializer

from todo.models import Task
from todo.serializer import (
    TaskSerializer,
    TaskCreateSerializer,
    TasksUpdateSerializer,
)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        """Retrieve the tasks with filters"""

        due_date = self.request.query_params.get("due_date")
        completed = self.request.query_params.get("completed")

        queryset = self.queryset.filter(user=self.request.user)

        if due_date:
            queryset = queryset.filter(due_date=due_date)

        if completed:
            queryset = queryset.filter(completed=completed)

        return queryset

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "create":
            self.serializer_class = TaskCreateSerializer
        if self.action == "update":
            self.serializer_class = TasksUpdateSerializer

        return self.serializer_class

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)
