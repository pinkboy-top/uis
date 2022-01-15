from django.urls import path
from user.views import reg_user

urlpatterns = [
    path('register', reg_user),
]
