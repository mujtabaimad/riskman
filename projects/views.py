from django.shortcuts import render
from . import models
from . import forms


def add_project(request):
    if request.method == 'POST' :
        project_data = models.Project(request.POST)
        if project_data.is_valid() :
            project = project_data.save(commit=False)
            project.save()
            return render(request,"success.html",{"name" : "khaled"})
        else :
            pass
    else :
        projectform = forms.ProjectForm()
        return render(request,"success.html",{"form" : projectform})
