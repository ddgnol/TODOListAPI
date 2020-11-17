from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response

from todo import models
from todo.models import Task
from todo.permissons import IsOwnerOrReadOnly
from todo.serializers import TaskSerializer, UserSerializer
from rest_framework import permissions


class ListTodo(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the tasks
        for the currently authenticated user.
        """
        user = self.request.user
        return Task.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        This view should return a list of all the tasks
        for the currently authenticated user.
        """
        user = self.request.user
        return Task.objects.filter(owner=user)

    permission_classes = [permissions.IsAuthenticated]
