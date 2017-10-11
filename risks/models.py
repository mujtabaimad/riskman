from django.db import models
from projects.models import Project, Task


class Case(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project)
    number_of_exe = models.IntegerField()


class Risk(models.Model):
    name = models.CharField(max_length=200)
    value = models.FloatField()
    tasks = models.ForeignKey(Task)

#
# 	def claculate(self):
# 		s = self.solve(self.root_node)
# 		self.result = str(s[0])
#
#
# 	def solve(self,s):
# 		if len(s.next_ids) == 0:
# 			return float(s.value+self.env['risk.node.risks'].search([('node','=',s.id),('risk','=',self.id)])[0].value)
# 		anss = []
# 		for i in range(len(s.next_ids)):
# 			anss.append(float(self.solve(s.next_ids[i])[0]))
# 		v = max(anss)
# 		return v+s.value+self.env['risk.node.risks'].search([('node','=',s.id),('risk','=',self.id)])[0].value
#
# class node_risk(models.Model):
# 	_name = 'risk.node.risks'
# 	node = models.ForeignKey('risk.node')
# 	risk = models.ForeignKey('risk.risks')
# 	value = models.Float()
#