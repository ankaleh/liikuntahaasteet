from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class Exercise(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.TextField(max_length=30)
    duration = models.IntegerField()
    date = models.DateField()

EXERCISES = [
    ('juoksu', 'juoksu'), 
    ('kävely', 'kävely'),
    ('kuntosaliliikunta', 'kuntosaliliikunta'),
    ('ryhmäliikunta', 'ryhmäliikunta'),
    ('luistelu', 'luistelu'),
    ('hiihto', 'hiihto'),
    ('jääkiekko', 'jääkiekko'),
    ('muu', 'muu')
]

class Challenge(models.Model):
    personChallenged = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personChallenged')
    challengedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challengedBy')
    exercise = models.TextField(max_length=30)
    duration = models.IntegerField()
    dateFrom = models.DateField()
    dateTo = models.DateField()

class DateInput(forms.DateInput):
    input_type = 'date'

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('exercise', 'duration', 'date')
        labels = {
            'exercise':'Laji',
            'duration':'Suorituksen kesto minuutteina',
            'date':'Ajankohta'
        }
        help_texts = {
            'exercise':'Valitse laji alaspudotusvalikosta.'
        }

        widgets = {
            'exercise': forms.Select(choices=EXERCISES),
            'date': DateInput()
        }

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('personChallenged', 'exercise', 'duration', 'dateFrom', 'dateTo')
        labels = {
            'exercise':'Laji',
            'duration':'Suorituksen kesto minuutteina',
            'dateFrom':'Mistä lähtien haaste on voimassa',
            'dateTo': 'Mihin asti haaste on voimassa',
            'personChallenged': 'Haastettava'
        }
        help_texts = {
           'personChallenged': 'Valitse alaspudotusvalikosta sen työtoverin nimi, jonka haluat haastaa.'
        }

        widgets = {
            'exercise': forms.Select(choices=EXERCISES),
            'dateTo': DateInput(),
            'dateFrom': DateInput()
        }

