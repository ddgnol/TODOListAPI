from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from todo.permissions import IsOwnerOrReadOnly
from todo.models import Task, Member
from todo.serializers import TaskSerializer
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


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def list_member(request, task_id=None):
    user = request.user
    if request.method == 'GET':
        task_list = Member.objects.filter(task=task_id)
        # print(task_list)
        member_list = []
        for task in task_list:
            member = {
                "id":task.user.id,
                "username":task.user.username
            }
            member_list.append(member)
        # print(member_list)
        return Response({"members": member_list}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            username = body['username']
        except:
            return Response({"message": "username is required"}, status=status.HTTP_400_BAD_REQUEST)
        task = Task.objects.filter(id=task_id).first()
        added_user = User.objects.filter(username=username).first()
        if task.owner != user:
            return Response({"message": "you are not owner of the task"}, status=status.HTTP_403_FORBIDDEN)
        if added_user is None:
            return Response({"message": "username is not available"}, status=status.HTTP_400_BAD_REQUEST)
        member = Member(user=added_user, task=task, role=2)
        member.save()
        return Response({"message": "add member OK"}, status=status.HTTP_200_OK)


@api_view(['DELETE', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def detail_member(request, task_id=None, user_id=None):
    user = request.user
    task = Task.objects.filter(id=task_id).first()
    changed_user = User.objects.filter(id=user_id).first()
    if task.owner != user:
        return Response({"message": "you are not owner of the task"}, status=status.HTTP_403_FORBIDDEN)
    if changed_user is None or Member.objects.filter(task=task).filter(user=changed_user).first() is None:
        return Response({"message": "invalid"}, status=status.HTTP_400_BAD_REQUEST)
    # if Member.objects.filter(id=task_id).filter(user=changed_user).first() is None:
    #     return Response({"message": "user is not a member of the task"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        Member.objects.filter(task=task).filter(user=changed_user).delete()
        return Response({"message": "delete member OK"}, status=status.HTTP_200_OK)
    if request.method == 'PATCH':

        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            role = body['role']
            # print(role)
        except:
            return Response({"message": "no change"}, status=status.HTTP_200_OK)

        if role <= 1:
            return Response({"message": "role not available"}, status=status.HTTP_400_BAD_REQUEST)
        Member.objects.filter(user=changed_user).update(role=role)
        return Response({"message": "update member OK"}, status=status.HTTP_200_OK)


# class AddMember(generics.GenericAPIView):
#     serializer_class = AddMemberSerializer
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
#
#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             task_id = request.data['task']
#             username = request.data['username']
#             task = Task.objects.filter(id=task_id).first()
#             added_user = User.objects.filter(username=username).first()
#             user = request.user
#             # print(user)
#             if task.owner != user:
#                 return Response({"message": "you are not owner of the task"}, status=status.HTTP_403_FORBIDDEN)
#             if task is None or added_user is None:
#                 return Response({"message": "task or user doesnt exist"}, status=status.HTTP_400_BAD_REQUEST)
#
#             member = Member(user=added_user, task=task, role=2)
#             member.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'add member successfully',
#                 # 'data': []
#             }
#
#             return Response(response)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
