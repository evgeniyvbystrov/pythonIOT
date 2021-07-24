from django.contrib import admin
from django.urls import path, include
from . import views

# Create your views here.
urlpatterns = [
    path('', views.graph, name='graph'),
    path('graph', views.graph,  name='graph'),
    path('tasks/', views.tasks, name='tasks'),
    path('devices/<str:device>/<str:state>', views.action_device, name='action_device')
    #    path('newtask/', views.newtask, name='newtask')
]