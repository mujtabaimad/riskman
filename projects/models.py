from django.db import models

import random

class Project(models.Model) :
    name = models.CharField(max_length=200)
    root_task = models.ForeignKey(Task)

class Task(models.Model):
    name = models.CharField(max_length=200)
    value = models.FloatField()
    project = models.ForeignKey(Project)

class TaskNext(models.Model):
    task = models.ForeignKey(Task)
    task_next = models.ForeignKey(Task)
    def __str__(self):
        return self.task.name + " : "+ self.task_next.name