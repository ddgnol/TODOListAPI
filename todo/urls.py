from django.urls import path
from todo import views
from rest_framework_simplejwt import views as jwt_views

from todo.views import ListTodo, DetailTodo

urlpatterns = [
    path('', ListTodo.as_view()),
    path('<int:pk>/', DetailTodo.as_view()),
]
