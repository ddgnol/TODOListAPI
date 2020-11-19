from django.urls import path

from users.views import RegisterView, LoginAPIView
from users import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('refresh-token/', views.refresh_token_view),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('<int:pk>/', views.UserView.as_view()),
]
