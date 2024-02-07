from django.shortcuts import render
from .models import TodoList
from rest_framework import generics
from .serializers import TodoSerializer

class TodoListAPIView(generics.ListAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoSerializer