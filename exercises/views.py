from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import *
from django.db.models import Sum

import os
import sys

def allJson(request):
    exercises = Exercise.objects.all()

    labels = []
    data = []
    #QuerySet  [{'exercise': 'juoksu', 'duration__sum': 2}, {'exercise': 'kävely', 'duration__sum': 1}, {'exercise': 'ryhmäliikunta', 'duration__sum': 1}]:
    querySet = Exercise.objects.values('exercise').annotate(Sum('duration'))

    for e in querySet:
        #print(e, file=sys.stderr)
        labels.append(e['exercise'])
        data.append(e['duration__sum'])

    print(labels, file=sys.stderr)
    print(data, file=sys.stderr)

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    

def charts(request):
    return render(request, 'charts.html')

def start(request):
    return render(request, 'start.html')

def loggingIn(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect('/oma-sivuni')
    else:
        # Return an 'invalid login' error message.
        return HttpResponse('Kirjautuminen ei onnistunut!')

def logout(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')

@login_required
def myPage(request):
    exercises = Exercise.objects.filter(person__pk=request.user.pk)
    return render(request, 'my_page.html', {'user': request.user, 'exercises': exercises})

@login_required
def addExercise(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.person = request.user
            exercise.save()
            messages.success(request, 'Suorituksen tallentaminen onnistui!')
            return redirect('/lisaa-uusi')
    else:
        form = ExerciseForm()
        #print(form, file=sys.stderr)
    return render(request, 'add_exercise.html', {'form': form })

@login_required
def secret(request):
    #print(request.user, file=sys.stderr)
    return HttpResponse("Salainen sivu")