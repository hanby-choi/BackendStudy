from django.contrib import admin
from django.urls import path, include
from .views import TodoListAPIView

urlpatterns = [
    path('api/todolist', TodoListAPIView.as_view(), name="todo-list"),
]