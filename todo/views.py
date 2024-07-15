from rest_framework import viewsets, permissions

from todo.models import Task
from todo.serializer import TaskSerializer, TaskCreateSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = TaskCreateSerializer

        return self.serializer_class

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)
