from django.urls import path
from rest_framework import routers

from todo import views

router = routers.DefaultRouter()
router.register("tasks", views.TaskViewSet)

urlpatterns = router.urls

app_name = "todo"
