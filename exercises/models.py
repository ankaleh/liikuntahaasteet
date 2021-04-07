from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class Exercise(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.TextField()
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
]

class DateInput(forms.DateInput):
    input_type = 'date'

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('exercise', 'duration', 'date')
        labels = {
            'exercise':'Laji',
            'duration':'Suorituksen kesto',
            'date':'Ajankohta'
        }
        help_texts = {
            'exercise':'Valitse laji alaspudotusvalikosta. '
        }

        widgets = {
            'exercise': forms.Select(choices=EXERCISES),
            'date': DateInput()
        }

