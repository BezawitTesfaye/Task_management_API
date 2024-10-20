# views.py
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Task
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth.models import User

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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    if request.method == 'POST':
        # Check if the request user has permission to create a new user
        if not request.user.has_perm('auth.add_user'):
            return Response({"detail": "You do not have permission to create a user."}, status=status.HTTP_403_FORBIDDEN)

        # Extract user data from the request
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate user data
        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username is already in use
        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, password=password)

        return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)

    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)