from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import os

def index(request):
    return HttpResponse("Hei, maailma!")

@login_required
def secret(request):
    return HttpResponse("Salainen sivu")