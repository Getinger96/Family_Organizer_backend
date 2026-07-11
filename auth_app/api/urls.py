from django.urls import path
from .views import RegistrationView, LoginParentView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginParentView.as_view(), name='login-parent'),
]