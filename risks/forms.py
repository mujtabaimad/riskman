from django.forms import ModelForm
from . import models


class CaseForm(ModelForm):
    class Meta:
        model = models.Case
        fields = ['name','project','number_of_exe']


class RiskForm(ModelForm):
    class Meta:
        model = models.Risk
        fields = ['name','probability']