from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
from . import forms


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
        return render(request,"order.html",{'tasks':tasks,'risks':risks,'case':case})


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