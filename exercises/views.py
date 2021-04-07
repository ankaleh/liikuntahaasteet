from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import ExerciseForm

import os
import sys

def index(request):
    return HttpResponse("Hei, maailma!")

def myView(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect('/salainen')
    else:
        # Return an 'invalid login' error message.
        return HttpResponse('Kirjautuminen ei onnistunut!')

def logout(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')

@login_required
def addExercise(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.person = request.user
            exercise.save()
            return redirect('/')
    else:
        form = ExerciseForm()
        print(form, file=sys.stderr)
    return render(request, 'add_exercise.html', {'form': form})

@login_required
def secret(request):
    print(request.user, file=sys.stderr)
    return HttpResponse("Salainen sivu")