from django.conf.urls import url
from django.urls import path

from users.views import RegisterView, LoginAPIView
from users import views

urlpatterns = [
    url('^register/?$', (RegisterView.as_view()), name="register"),
    url(r'^login/?$', (LoginAPIView.as_view())),
    url(r'^refresh-token/?$', views.refresh_token_view, name='refresh-token'),
    url(r'^change-password/?$', (views.ChangePasswordView.as_view()), name='change-password'),
    # path('/<int:pk>', views.UserView.as_view()),
]
