from .models import Tasks, IOTData
from django.forms import ModelForm, TextInput, DateTimeInput, DecimalField

class TaskForm (ModelForm):
    class Meta:
        model = Tasks
        fields = ['device', 'task', 'datetime']
        widgets = {'device': TextInput(attrs={'class':'form-control','placeholder': 'Введите название датчика'}),
                   'datetime': DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Введите дату'}),
                   'task': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите команду'})
                   }