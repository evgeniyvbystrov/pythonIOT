from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import IOTData, Tasks
from .forms import TaskForm
from .figures import get_plot, get_devices, set_current_state


def action_device(request, device, state):
    set_current_state(device, state)
    return HttpResponseRedirect('/graph')

def graph(request):

    devices = get_devices()
    chart = get_plot()
    return render(request, 'graps/graph.html', {'chart': chart, 'devices': devices})


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
        'form': form,
        'title': 'Выберите датчик'
    }
    return render(request, 'graps/newtask.html', context)