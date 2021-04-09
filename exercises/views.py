from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import *
from django.db.models import Sum

import os
import sys

@login_required
def allJson(request):
    labels = []
    data = []
    #QuerySet  [{'exercise': 'juoksu', 'duration__sum': 2}, {'exercise': 'kävely', 'duration__sum': 1}, {'exercise': 'ryhmäliikunta', 'duration__sum': 1}]:
    durationPerExercise = Exercise.objects.values('exercise').annotate(Sum('duration'))

    for e in durationPerExercise:
        labels.append(e['exercise'])
        data.append(e['duration__sum'])

    data, labels = zip(*sorted(zip(data, labels)))

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required
def myJson(request):
    exercisesInAll = []
    durationsInAll = []
    datesInAll = []

    minutes = []
    dates = []

    durations = []
    exercises = []

    allExercises = Exercise.objects.filter(person__pk=request.user.pk)

    durationPerExercise = Exercise.objects.values('exercise').annotate(Sum('duration')).filter(person__pk=request.user.pk)

    minutesInDay = Exercise.objects.values('date').annotate(Sum('duration')).filter(person__pk=request.user.pk) #8
    
    for e in allExercises:
        exercisesInAll.append(e.exercise)
        durationsInAll.append(e.duration)
        datesInAll.append(e.date)

    for i in minutesInDay:
        dates.append(i['date'])
        minutes.append(i['duration__sum'])
    
    for e in durationPerExercise:
        exercises.append(e['exercise'])
        durations.append(e['duration__sum'])
    
    return JsonResponse(data={
        'all': {
            'exercises': exercisesInAll,
            'durations': durationsInAll,
            'dates': datesInAll,
        },
        'minutesInDay': {
            'minutes': minutes,
            'dates': dates,
        },
        'durationPerExercise': {
            'exercises': exercises,
            'durations': durations,
        },
        
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