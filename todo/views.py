from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from todo.permissions import IsOwnerOrReadOnly
from todo.models import Task, Member
from todo.serializers import TaskSerializer, AddMemberSerializer
from rest_framework import permissions

from users.models import User


class ListTodo(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        """
        This view should return a list of all the tasks
        for the currently authenticated user.
        """
        user = self.request.user
        all_tasks = Member.objects.filter(user=user)
        pk_list = []
        for t in all_tasks:
            pk_list.append(t.task.id)
        # print(pk_list)
        return Task.objects.filter(pk__in=pk_list)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # # print(self.request.user)
        task = Task.objects.filter(owner=self.request.user).order_by('-pub_date')[0]
        print(task)
        member = Member(user=self.request.user, task=task, role=1)
        member.save()


class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        This view should return a list of all the tasks
        for the currently authenticated user.
        """
        user = self.request.user
        all_tasks = Member.objects.filter(user=user)
        pk_list = []
        for t in all_tasks:
            pk_list.append(t.task.id)
        # print(pk_list)
        return Task.objects.filter(pk__in=pk_list)


class AddMember(generics.GenericAPIView):
    serializer_class = AddMemberSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            task_id = request.data['task']
            username = request.data['username']
            task = Task.objects.filter(id=task_id).first()
            added_user = User.objects.filter(username=username).first()
            user = request.user
            # print(user)
            if task.owner != user:
                return Response({"message": "you are not owner of the task"}, status=status.HTTP_403_FORBIDDEN)
            if task is None or added_user is None:
                return Response({"message": "task or user doesnt exist"}, status=status.HTTP_400_BAD_REQUEST)

            member = Member(user=added_user, task=task, role=2)
            member.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'add member successfully',
                # 'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
