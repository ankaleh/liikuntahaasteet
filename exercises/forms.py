from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


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

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name

class DateInput(forms.DateInput):
    input_type = 'date'

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('exercise', 'duration', 'date')
        labels = {
            'exercise':'Laji',
            'duration': 'Suorituksen kesto minuutteina',
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
            'duration':'Harjoiteltava vähintään',
            'dateFrom':'Mistä lähtien haaste on voimassa',
            'dateTo': 'Mihin asti haaste on voimassa',
            'personChallenged': 'Haastettava'
        }
        field_classes = {
            'personChallenged': UserModelChoiceField
        }
        help_texts = {
           'personChallenged': 'Valitse alaspudotusvalikosta sen työtoverin nimi, jonka haluat haastaa. Jos haluat haastaa itsesi, valitse oma nimesi.',
           'duration': 'Merkitse, kuinka monta minuuttia vähintään ajanjakson aikana on liikuttava. Esimerkiksi jos ajanjakso on noin neljä viikkoa ja haastat liikkumaan neljä tuntia viikossa, merkitse tähän 960 minuuttia.'
        }
        widgets = {
            'exercise': forms.Select(choices=EXERCISES),
            'dateTo': DateInput(),
            'dateFrom': DateInput()
        }

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Etunimi')
    last_name = forms.CharField(max_length=30, required=False, help_text='Sukunimi ei ole pakollinen tieto.', label='Sukunimi')
    password1 = forms.CharField(
        label='Salasana',
        widget=forms.PasswordInput,
        help_text='Salasanan on oltava vähintään 8 merkkiä pitkä, eikä se saa muodostua pelkistä numeroista.'
    )
    password2 = forms.CharField(
        label='Salasanan varmistus',
        widget=forms.PasswordInput,
        help_text='Anna salasana toisen kerran.'
    )
    class Meta:
        model = User
        labels = {
            'username':'Käyttäjätunnus',
        }
        fields = ('first_name', 'last_name', 'username')
        help_texts = {
            'username':'Anna käyttäjätunnus.'
        }
        