from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
from projects import models as mo
from . import forms
import random


def add_case(request):
    if request.method == 'POST' :
        case_data = forms.CaseForm(request.POST)
        if case_data.is_valid() :
            case = case_data.save(commit=False)
            case.save()
            return redirect("/cases/"+str(case.id)+"/risks/")
        else :
            pass
    else :
        caseform = forms.CaseForm()
        return render(request,"case_new.html",{"form" : caseform})


def add_risk(request,id):
    if request.method == 'POST' :
        risk_data = forms.RiskForm(request.POST)
        if risk_data.is_valid() :
            risk = risk_data.save(commit=False)
            risk.case_id = id
            risk.save()
            return redirect("/cases/"+str(id)+"/risks/")
        else :
            pass
    else :
        case = models.Case.objects.get(id=id)
        risks = case.risk_set.get_queryset()
        case_risks_form = forms.RiskForm()
        return render(request,"add_risk.html",{"form" : case_risks_form,'risks':risks,'case':case})


def del_risk(request,id,t_id):
    risk = models.Risk.objects.get(id=t_id)
    risk.delete()
    return  redirect("/cases/"+str(id)+"/risks")


def edit_risk(request,id,t_id):
    risk = models.Risk.objects.get(id=t_id)
    if request.method == 'POST' :
        risl_data = forms.RiskForm(request.POST)
        if risl_data.is_valid() :
            risk.probability = request.POST.get("probability")
            risk.name = request.POST.get("name")
            risk.save()
            return redirect("/cases/"+str(id)+"/risks/")
        else :
            pass
    else :
        case = models.Case.objects.get(id=id)
        risks = case.risk_set.get_queryset()
        case_risks_form = forms.RiskForm()
        return render(request, "add_risk.html", {"form": case_risks_form, 'risks': risks, 'case': case})


def assign_tasks(request,id):
    if request.method == 'GET' :
        case = models.Case.objects.get(id=id)
        project = case.project
        tasks = project.task_set.get_queryset()
        risks = case.risk_set.get_queryset()

        assos_tasks = models.Risk_task.objects.filter(task__in=[task for task in tasks])
        # nextTasksFull = []
        # for i in nextTasks:
        #     nextTasksFull.append({'id':i.task,'name':models.Task.objects.get(id=i.task_next).name})
        return render(request,"assign_tasks.html",{'tasks':tasks,'risks':risks,'case':case,'assos_tasks':assos_tasks})


@csrf_exempt
def assign_risk_task(request):
    if request.method == 'POST' :
        risk_id = request.POST.get('risk_id', '')
        task_id = request.POST.get("task_id",'')
        duration = request.POST.get("duration",'')
        cost = request.POST.get("cost",'')
        risk_task = models.Risk_task()
        # print(risk_id,task_id)
        risk_task.task = models.Task.objects.get(id=task_id)
        risk_task.risk = models.Risk.objects.get(id=risk_id)
        risk_task.duration = duration
        risk_task.cost = cost
        risk_task.save()
        return JsonResponse({'status':0})
    else:
        print('get')


def result(request,id):
    if request.method == 'POST':
        pass
    else:
        case = models.Case.objects.get(id=id)
        risks = case.risk_set.get_queryset()
        project = case.project
        tasks = project.task_set.get_queryset()
        all = []
        w = []
        for kk in range(case.number_of_exe):
            new_tasks={}
            risks_to_mod = get_rand_risks(risks)
            print(risks_to_mod)
            for i in tasks:
                nextTasks = mo.TaskNext.objects.filter(task__in=[i.id])
                risks_task = models.Risk_task.objects.filter(task__in=[i.id])
                for ll in risks_task:
                    print('---',ll.risk.id)
                print()
                d = i.duration
                c = i.cost
                for j in risks_task:
                    if j.risk.id in risks_to_mod:
                        d+=j.duration
                        c+=j.cost
                new_tasks[str(i.id)]= {"duration":d,"cost":c,'next':nextTasks}
                # print(i.name,nextTasks,"==================")
            res = calc({'risks':risks,'case':case,'new_tasks':new_tasks,'root':tasks[0]})
            w.append(res)
            all.append({'tasks':tasks,'risks':risks,'case':case,'new_tasks':new_tasks,'root':tasks[0],'result':res,'mod':risks_to_mod})

        return render(request,"result.html",{'all':all,'worst_case':max(w)})


def calc(data):
    s = solve(data['root'],data['new_tasks'])
    return s


def solve(root,new_tasks):
    # print (str(root),"------------------------------------")
    if len(new_tasks[str(root.id)]['next']) == 0:
        return new_tasks[str(root.id)]['duration']+root.duration
    anss = []
    for i in new_tasks[str(root.id)]['next']:
        new_root = models.Task.objects.get(id=i.task_next)
        anss.append(float(solve(new_root,new_tasks)))
    v = max(anss)
    return v+root.duration
    pass


def get_rand_risks(risks):
    result = []
    for i in risks:
        r = random.uniform(0, 100)
        if i.probability <= r:
            result.append(i.id)
    return result
# def claculate(tasks,new_tasks):
#     s = self.solve(self.root_node)
#     self.result = str(s[0])
#
#
# def solve(self,s):
#     if len(s.next_ids) == 0:
#         return float(s.value+self.env['risk.node.risks'].search([('node','=',s.id),('risk','=',self.id)])[0].value)
#     anss = []
#     for i in range(len(s.next_ids)):
#         anss.append(float(self.solve(s.next_ids[i])[0]))
#     v = max(anss)
#     return v+s.value+self.env['risk.node.risks'].search([('node','=',s.id),('risk','=',self.id)])[0].value