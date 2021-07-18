from django.contrib import admin
from django.urls import path, include
from . import views

# Create your views here.
urlpatterns = [
    path('graph/', views.graph,  name='graph'),
    path('tasks/', views.tasks, name='tasks'),
    path('newtask/', views.newtask, name='newtask')
]