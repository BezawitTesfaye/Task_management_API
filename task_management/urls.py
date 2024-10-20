from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TaskViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]