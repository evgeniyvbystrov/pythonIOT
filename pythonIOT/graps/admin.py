from django.contrib import admin

# Register your models here.
from .models import IOTData, Tasks

admin.site.register(IOTData)
admin.site.register(Tasks)
