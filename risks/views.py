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
        all = {}
        total_cost = 0
        for kk in range(case.number_of_exe):
        # for kk in range(10):
            new_tasks={}
            i_cost = 0
            risks_to_mod = get_rand_risks(risks)
            selected_risks = [models.Risk.objects.get(id=i) for i in risks_to_mod]
            #print(risks_to_mod)
            if tuple(selected_risks) in all.keys():
                total_cost+=all[tuple(selected_risks)]['cost']
                all[tuple(selected_risks)]['count']+=1
            else:
                for i in tasks:
                    nextTasks = mo.TaskNext.objects.filter(task__in=[i.id])
                    risks_task = models.Risk_task.objects.filter(task__in=[i.id])

                    d = i.duration
                    c = i.cost
                    i_cost+=i.cost
                    for j in risks_task:
                        if j.risk.id in risks_to_mod:
                            d+=j.duration
                            c+=j.cost
                            i_cost+=j.cost
                    new_tasks[str(i.id)]= {"duration":d,"cost":c,'next':nextTasks}
                    # print(i.name,nextTasks,"==================")
                res = calc({'new_tasks':new_tasks,'root':tasks[0]})
                total_cost+=i_cost

                all[tuple(selected_risks)] = {'cost':i_cost,'result':res,'new_tasks':new_tasks,'count':1}

        return render(request,"result.html",{
                          'tasks':tasks,
                          'risks':risks,
                          'case':case,
                          'root':tasks[0],
                          'all':all,
                          'worst_case_value':get_max(all)[1],
                          'worst_case_cost':get_max(all)[2],
                          'worst_case':get_max(all)[0],
                          'most_case_value':get_max(all)[4],
                          'most_case_cost':get_max(all)[5],
                          'most_case':get_max(all)[3],
                          'average_cost':"{0:.2f}".format(round(total_cost/case.number_of_exe,2)),
                          'average_duration':"{0:.2f}".format(round(get_average(all),2)),
                      })


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
        if i.probability >= r:
            result.append(i.id)
    return result

def get_average(all):
    duration_avg = 0
    for key, value in all.items():
        duration_avg+= value['result']/len(all)

    return duration_avg

def get_max(all):
    m = -10000000000
    c = 0
    m_d = 0
    m_c = 0
    count = 0
    m_selected_risks_ids = False
    selected_risks_ids= False
    for key, value in all.items():
        to_compare = [i.id for i in key]
        if value['result'] > m:
            m = value['result']
            selected_risks_ids = to_compare
            c = value['cost']
        if value['count'] > count:
            m_d = value['result']
            m_selected_risks_ids = to_compare
            m_c = value['cost']
            count = value["count"]

    selected_risks = [models.Risk.objects.get(id=i) for i in selected_risks_ids]
    m_selected_risks = [models.Risk.objects.get(id=i) for i in m_selected_risks_ids]
    return selected_risks,m,c,m_selected_risks,m_d,m_c

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