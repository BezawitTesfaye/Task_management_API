from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .task_management.views import BookViewSet, TransactionViewSet, UserViewSet, TaskViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
]