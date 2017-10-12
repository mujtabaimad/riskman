from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
from . import forms


def add_project(request):
    if request.method == 'POST' :
        project_data = forms.ProjectForm(request.POST)
        if project_data.is_valid() :
            project = project_data.save(commit=False)
            project.save()
            return redirect("/projects/"+str(project.id)+"/tasks/")
        else :
            pass
    else :
        projectform = forms.ProjectForm()
        return render(request,"project_new.html",{"form" : projectform})


def add_task(request,id):
    if request.method == 'POST' :
        task_data = forms.TaskForm(request.POST)
        if task_data.is_valid() :
            task = task_data.save(commit=False)
            task.project_id = id
            task.save()
            return redirect("/projects/"+str(id)+"/tasks/")
        else :
            pass
    else :
        project = models.Project.objects.get(id=id)
        tasks = project.task_set.get_queryset()
        projects_tasks_form = forms.TaskForm()
        return render(request,"add_task.html",{"form" : projects_tasks_form,'tasks':tasks,'project':project})


def order(request,id):
    if request.method == 'GET' :
        project = models.Project.objects.get(id=id)
        tasks = project.task_set.get_queryset()
        nextTasks = models.TaskNext.objects.filter(task__in=[task.id for task in tasks])
        nextTasksFull = []
        for i in nextTasks:
            nextTasksFull.append({'id':i.task,'name':models.Task.objects.get(id=i.task_next).name})
        # print(nextTasksFull)
        return render(request,"order.html",{'tasks':tasks,'project':project,'nextTasks':nextTasksFull})


@csrf_exempt
def order_tasks(request):
    if request.method == 'POST' :
        id = request.POST.get('id', '')
        next = request.POST.getlist("next")
        task = models.Task.objects.get(id=int(id))
        for i in next:
            task_next = models.TaskNext()
            task_next.task = task.id
            task_next.task_next = i
            task_next.save()
        return JsonResponse({'status':0})

def del_task(request,id,t_id):
    task = models.Task.objects.get(id=t_id)
    task.delete()
    return  redirect("/projects/"+str(id)+"/tasks")
def edit_task(request,id,t_id):
    task = models.Task.objects.get(id=t_id)
    if request.method == 'POST' :
        task_data = forms.TaskForm(request.POST)
        if task_data.is_valid() :
            task.cost = request.POST.get("cost")
            task.duration = request.POST.get("duration")
            task.name = request.POST.get("name")
            task.save()
            return redirect("/projects/"+str(id)+"/tasks/")
        else :
            pass
    else :
        project = models.Project.objects.get(id=id)
        tasks = project.task_set.get_queryset()
        projects_tasks_form = forms.TaskForm(instance=task)
        return render(request,"add_task.html",{"form" : projects_tasks_form,'tasks':tasks,'project':project})

def allprojects(request):
    projects = models.Project.objects.all()
