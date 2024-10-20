# views.py
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Task
from rest_framework.response import Response
from rest_framework.decorators import action

class TaskViewSet(viewsets.ModelViewSet):

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.mark_as_complete()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def incomplete(self, request, pk=None):
        task = self.get_object()
        task.mark_as_incomplete()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
        filter_backends = [filters.OrderingFilter]
    ordering_fields = ['due_date', 'priority']
    ordering = ['due_date', 'priority']

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        
        status = self.request.query_params.get('status', None)
        if status:
            if status.lower() == 'pending':
                queryset = queryset.filter(completed=False)
            elif status.lower() == 'completed':
                queryset = queryset.filter(completed=True)

        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)

        due_date = self.request.query_params.get('due_date', None)
        if due_date:
            queryset = queryset.filter(due_date=due_date)

        return queryset

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ['id', 'username', 'email']

    def list(self, request):
        queryset = CustomUser.objects.filter(id=request.user.id)
        serializer = self.UserSerializer(queryset, many=True)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    class TaskSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            fields = ['id', 'title', 'description', 'user', 'completed', 'completed_at', 'priority', 'due_date']

    def list(self, request):
        queryset = Task.objects.filter(user=request.user)
        serializer = self.TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)