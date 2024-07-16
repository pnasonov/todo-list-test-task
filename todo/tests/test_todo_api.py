import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from todo.models import Task
from todo.serializer import TaskSerializer

TODO_URL = reverse("todo:task-list")


def sample_task(**params):
    defaults = {
        "title": "Sample Task",
        "description": "This is a sample task",
        "due_date": datetime.date.today(),
        "completed": False,
    }
    defaults.update(params)

    return Task.objects.create(**defaults)


def detail_url(task_id):
    return reverse("todo:task-detail", args=[task_id])


class UnauthenticatedTodoApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TODO_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedTodoApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@example.com", "test_password"
        )
        self.client.force_authenticate(self.user)

    def test_list_tasks(self):
        sample_task(user=self.user)
        sample_task(user=self.user)

        res = self.client.get(TODO_URL)

        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_list_tasks_pagination_for_5_items(self):
        for i in range(6):
            sample_task(user=self.user)

        res = self.client.get(TODO_URL)

        self.assertEqual(len(res.data["results"]), 5)

    def test_filter_tasks_by_due_date(self):
        task1 = sample_task(user=self.user, due_date=datetime.date.today())
        task2 = sample_task(
            user=self.user,
            due_date=datetime.date.today() + datetime.timedelta(days=1),
        )
        task3 = sample_task(
            user=self.user,
            due_date=datetime.date.today() + datetime.timedelta(days=2),
        )

        res = self.client.get(TODO_URL, {"due_date": datetime.date.today()})

        serializer1 = TaskSerializer(task1)
        serializer2 = TaskSerializer(task2)
        serializer3 = TaskSerializer(task3)

        self.assertIn(serializer1.data, res.data["results"])
        self.assertNotIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])

    def test_filter_tasks_by_completed(self):
        task1 = sample_task(user=self.user, completed=True)
        task2 = sample_task(user=self.user, completed=True)
        task3 = sample_task(user=self.user, completed=False)

        res = self.client.get(TODO_URL, {"completed": True})

        serializer1 = TaskSerializer(task1)
        serializer2 = TaskSerializer(task2)
        serializer3 = TaskSerializer(task3)

        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])

    def test_create_task(self):
        payload = {
            "title": "Sample Task",
            "description": "This is a sample task",
            "due_date": str(datetime.date.today()),
        }
        res = self.client.post(TODO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, res.data | payload)

    def test_create_tasks_with_inappropriate_date(self):
        payload = {
            "title": "Sample Task",
            "description": "This is a sample task",
            "due_date": datetime.date.today() - datetime.timedelta(days=1),
        }
        res = self.client.post(TODO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_task_detail(self):
        task = sample_task(user=self.user)

        url = detail_url(task.id)
        res = self.client.get(url)

        serializer = TaskSerializer(task)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_task(self):
        task = sample_task(user=self.user)
        update_payload = {
            "description": "New description",
            "completed": True,
        }

        url = detail_url(task.id)
        res = self.client.put(url, update_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, res.data | update_payload)

    def test_delete_task(self):
        task = sample_task(user=self.user)

        url = detail_url(task.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.filter(id=task.id).exists(), False)
