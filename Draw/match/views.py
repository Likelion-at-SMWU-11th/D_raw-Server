from django.shortcuts import render
from .models import MatchUser
from .forms import MatchBasedForm

def match(request):
    form = MatchBasedForm()
    return render(request, 'match.html', {'form' : form})

def check(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    return render(request, 'check.html')

def quick(request):
    return render(request, 'quick.html')

def profile(request):
    return render(request, 'profile.html')