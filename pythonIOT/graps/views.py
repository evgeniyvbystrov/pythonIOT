from django.shortcuts import render, redirect
from .models import IOTData, Tasks
from .forms import TaskForm
from .figures import get_plot,my_figure


def graph(request):

    chart = get_plot()
    return render(request, 'graps/graph.html', {'chart': chart})


def tasks(request):

    tasks = Tasks.objects.all()
    return render(request, 'graps/tasks.html', {'tasks': tasks})


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