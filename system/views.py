from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
import forms
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, 'index.html', {'button_group': True})


def login(request):
    if request.method == 'POST':
        username = request.POST['account']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None: 
            if user.is_active:
                auth.login(request, user)
                return render(request, 'datashow.html')
        else:
            form = forms.LoginForm()
            return render(request, 'login.html', {'error': 'Account or password incorrect.', 'form': form})
    else:
        form = forms.LoginForm()
    return render(request, 'login.html', {'form': form})


def registe(request):
    if request.method == 'POST':
        username = request.POST['account']
        password = request.POST['confirmpassword']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        new_user = auth.authenticate(username=username, password=password)
        if new_user is not None:
            auth.login(request, new_user)
            return HttpResponse('registe and login success.')
    else:
        form = forms.RegisteForm()
    return render(request, 'registe.html', {'form': form})


def logout(request):
    auth.logout(request)
    return render(request, 'index.html', {'button_group': True})


@login_required
def datashow(request):
    return render(request, 'datashow.html')