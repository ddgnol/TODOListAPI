"""CustomUser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include


from users import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('users/', include('users.urls'), name='users'),
    path('todo/', include('todo.urls'), name='todo'),
    # path('profile', views.UserView.as_view()),
    url(r'^profile/?$', views.profile)
]
handler500 = 'users.utils.server_error'
handler400 = 'rest_framework.exceptions.bad_request'
