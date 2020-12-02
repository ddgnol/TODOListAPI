from django.conf.urls import url
from django.urls import path
from jsonview.decorators import json_view

from todo.models import Member
from todo.views import ListTodo, DetailTodo
from todo import views

urlpatterns = [
    url(r'(?P<task_id>[0-9]+)/member/(?P<user_id>[0-9]+)/?', views.detail_member),
    url(r'(?P<task_id>[0-9]+)/member/?', views.list_member),
    url(r'^list/?$', (ListTodo.as_view())),
    url(r'(?P<pk>[0-9]+)/?', (DetailTodo.as_view())),
    # url(r'^add-member/?$', AddMember.as_view()),

    # path('<int:task_id>'
]
