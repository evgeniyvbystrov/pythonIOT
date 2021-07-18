from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import IOTData, Tasks
from .forms import TaskForm

def graph(request):
    iotdata = IOTData.objects.all()
    return render(request, 'graps/graph.html', {'iotdata': iotdata} )

def tasks(request):
    tasks = Tasks.objects.all()
    return render(request, 'graps/tasks.html', {'tasks': tasks} )

def newtask(request):

    if request.method == 'post':
        form = TaskForm(request.POST)
        #if form.is_valid():
        #    form.save()
        redirect('tasks')

    form = TaskForm()
    context = {
        'form':form,
        'title':'Выберите датчик'
    }
    return render(request, 'graps/newtask.html', context)