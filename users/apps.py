import logging

from django.apps import AppConfig
from rest_framework import status, request
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import exception_handler
from CustomUser.logger import SlackHandler
from CustomUser.logger import Logger
import traceback


class UsersConfig(AppConfig):
    name = 'users'


