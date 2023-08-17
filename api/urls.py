from django.urls import path
from .views import *

urlpatterns = [
  path('login/', LoginApi.as_view()),
  path('register/', RegisterApi.as_view()),
]