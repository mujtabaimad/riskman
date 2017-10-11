from django.db import models

import random



class Project(models.Model) :
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    root_task = models.IntegerField(null=True)


class Task(models.Model):
    name = models.CharField(max_length=200)
    duration = models.FloatField()
    cost = models.FloatField()
    project = models.ForeignKey(Project)
    def __str__(self):
        return self.name


class TaskNext(models.Model):
    task = models.IntegerField()
    task_next = models.IntegerField()
    # def __str__(self):
    #     return self.task.name + " : "+ self.task_next.name    # def __str__(self):
    #     return self.task.name + " : "+ self.task_next.name