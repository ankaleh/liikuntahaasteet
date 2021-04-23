from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your models here.

class Exercise(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.TextField(max_length=30)
    duration = models.IntegerField()
    date = models.DateField()

class Challenge(models.Model):
    personChallenged = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personChallenged')
    challengedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challengedBy')
    exercise = models.TextField(max_length=30)
    duration = models.IntegerField()
    dateFrom = models.DateField()
    dateTo = models.DateField()

    def __str__(self):
        return f"{self.personChallenged.first_name}"

class Completer(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completer')
    def __str__(self):
        return f"{self.person.first_name}"

class EmployerChallenge(models.Model):
    exercise = models.TextField(max_length=30)
    duration = models.IntegerField()
    dateFrom = models.DateField()
    dateTo = models.DateField()
    carrot = models.TextField(max_length=50)
    completers = models.ManyToManyField(Completer, related_name='completers')

    def __str__(self):
        compls = ', '.join(str(c.person.first_name) for c in self.completers.all())
        return f"{self.exercise}, {self.dateTo}, {compls}"

