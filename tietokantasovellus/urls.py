"""tietokantasovellus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import exercises.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kirjaudu/', auth_views.LoginView.as_view(template_name='login.html')),
	path('kirjaudu-ulos/', auth_views.LogoutView.as_view(next_page='/')),
    

    path('', exercises.views.start, name='start'),
    path('salainen/', exercises.views.secret, name='secret'),
    path('lisaa-uusi/', exercises.views.addExercise, name='addExercise'),
    path('haasta/', exercises.views.challenge, name='challenge'),
    path('oma-sivuni/', exercises.views.myPage, name='myPage'),
    path('kirjaudutaan/', exercises.views.loggingIn, name='loggingIn'),
    path('tilastot/', exercises.views.charts, name='charts'),
    path('rekisteroidy', exercises.views.signup, name='signup'),

    path('all-json/', exercises.views.allJson, name='allJson'),
    path('my-json/', exercises.views.myJson, name='myJson'),
    path('remove-challenge/<int:challenge_id>', exercises.views.removeChallenge, name='removeChallenge'),
]
