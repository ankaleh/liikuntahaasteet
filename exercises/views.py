from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *
from django.db.models import Sum
from django.db.models import Q

import os
import sys
from datetime import date

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/oma-sivuni')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def allJson(request):
    labels = []
    data = []

    durationPerExercise = Exercise.objects.values('exercise').annotate(Sum('duration'))

    for e in durationPerExercise:
        labels.append(e['exercise'])
        data.append(e['duration__sum'])

    if  len(data) > 0:
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
    durationAllExercises = Exercise.objects.filter(person__pk=request.user.pk).aggregate(Sum('duration'))
    minutesInDay = Exercise.objects.values('date').annotate(Sum('duration')).filter(person__pk=request.user.pk)

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
        return redirect('/oma-sivuni')
    else:
        messages.error(request, 'Käyttäjänimeä ei löydy tai salasana on virheellinen. Yritä uudestaan!')
        return redirect('/kirjaudu')

@login_required
def removeChallenge(request, challenge_id):
    if Challenge.objects.filter(id=challenge_id).exists():
        challenge = Challenge.objects.get(id=challenge_id)
        challenge.delete()
        messages.info(request, 'Haaste poistettiin!')
        return redirect('/oma-sivuni')

def logout(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')

@login_required
def myPage(request):
    #haetaan haasteet, joissa käyttäjä on osallisena
    challenges = Challenge.objects.filter(challengedBy__pk=request.user.pk) | Challenge.objects.filter(personChallenged__pk=request.user.pk) 
    if len(challenges) > 0:
        messages.info(request, 'Sinulla on käynnissä olevia haasteita!')

    #progression-taulukoissa haasteet kirjasto-kokoelmina, joissa avaimina haasteen id,
    #haasteeseen vastaavien harjoitusten kestojen summa sekä kuinka paljon haasteesta on vielä tekemättä
    progression = [] 
    progressionOther = []
    exercisesOther = []
    employerChallenge = None
    #haetaan voimassa oleva työnantajan haaste:
    if EmployerChallenge.objects.filter(dateFrom__lte=date.today(), dateTo__gte=date.today()).exists():
        #lisätään progression-taulukkoon tieto edistymisestä työnantajan haasteen parissa:
        employerChallenge = EmployerChallenge.objects.get(dateFrom__lte=date.today(), dateTo__gte=date.today())
        progressionWithEmployerChallenge = Exercise.objects.values('exercise').annotate(Sum('duration')).filter(exercise=employerChallenge.exercise, date__gte=employerChallenge.dateFrom, date__lte=employerChallenge.dateTo, person__pk=request.user.pk)
        if len(progressionWithEmployerChallenge) > 0:
            progression.append({'challenge_id': 'employer-challenge', 'done': progressionWithEmployerChallenge[0]['duration__sum'], 'to_do': employerChallenge.duration - progressionWithEmployerChallenge[0]['duration__sum'] })
            if progressionWithEmployerChallenge[0]['duration__sum']>=employerChallenge.duration and not Completer.objects.filter(person=request.user).exists():
                messages.success(request, 'Onneksi olkoon! Olet täyttänyt työnantajan asettaman haasteen! Palkintosi on {}!'.format(employerChallenge.carrot))
                completer = Completer(person=request.user)
                completer.save()
                employerChallenge.completers.add(completer)

    for c in challenges:
        #lasketaan omien tähän haasteeseen vastaavien harjoitusten kestot yhteen:
        exercisesOwn = Exercise.objects.values('exercise').annotate(Sum('duration')).filter(exercise=c.exercise, date__gte=c.dateFrom, date__lte=c.dateTo, person__pk=request.user.pk)
        if c.challengedBy.pk == request.user.pk:
            #lasketaan haastetun tähän haasteeseen vastaavien harjoitusten kestot yhteen:
            exercisesOther = Exercise.objects.values('exercise').annotate(Sum('duration')).filter(exercise=c.exercise, date__gte=c.dateFrom, date__lte=c.dateTo, person__pk=c.personChallenged.pk)
        else:
            exercisesOther = Exercise.objects.values('exercise').annotate(Sum('duration')).filter(exercise=c.exercise, date__gte=c.dateFrom, date__lte=c.dateTo, person__pk=c.challengedBy.pk)
        for e in exercisesOwn:
            if e['duration__sum']>=c.duration:
                messages.success(request, 'Onneksi olkoon! Olet täyttänyt haasteen, jonka sinulle antoi {}!'.format(c.challengedBy.first_name))
            progression.append({'challenge_id':c.id, 'done': e['duration__sum'], 'to_do': c.duration - e['duration__sum'] })
        for e in exercisesOther:
            progressionOther.append({'challenge_id':c.id, 'done': e['duration__sum'], 'to_do': c.duration - e['duration__sum'] })

    return render(request, 'my_page.html', {'user': request.user, 'challenges': challenges, 'progression': progression, 'progressionOther': progressionOther, 'employerChallenge': employerChallenge})

@login_required
def addExercise(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.person = request.user
            exercise.save()
            messages.info(request, 'Suorituksen tallentaminen onnistui!')
            return redirect('/lisaa-uusi')
    else:
        form = ExerciseForm()
        
    return render(request, 'add_exercise.html', {'form': form })

@login_required
def challenge(request):
    if request.method == "POST":
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.challengedBy = request.user
            challenge.save()
            messages.info(request, 'Haaste välitetty!')
            return redirect('/haasta')
    else:
        form = ChallengeForm()
        
    return render(request, 'challenge.html', {'form': form })

@login_required
def secret(request):
    return HttpResponse("Salainen sivu")