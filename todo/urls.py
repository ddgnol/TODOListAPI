from django.conf.urls import url
from django.urls import path
from jsonview.decorators import json_view

from todo.views import ListTodo, DetailTodo

urlpatterns = [
    url(r'^list/?$', json_view(ListTodo.as_view())),
    url(r'(?P<pk>[0-9]+)/?$', json_view(DetailTodo.as_view())),
]
