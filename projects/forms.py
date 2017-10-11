from django.forms import ModelForm
from . import models


class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = ['name','owner']

class TaskForm(ModelForm):
    class Meta:
        model = models.Task
        fields = ['name','duration','cost']
