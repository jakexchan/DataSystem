from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import forms

from models import UserInfo, WeiboInfo
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
                return HttpResponseRedirect('/datashow/user/1')
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
            return HttpResponseRedirect('/datashow/user/1')
    else:
        form = forms.RegisteForm()
    return render(request, 'registe.html', {'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def user_table(request, page):
    all_user_lists = UserInfo.objects.all();
    all_weibo_lists = WeiboInfo.objects.all();
    paginator = Paginator(all_user_lists, 11)
    try:
        lists = paginator.page(page)
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)
    return render(request, 'usershow.html', { 'lists': lists, 'weibo_list_count': len(all_weibo_lists)})


@login_required
def weibo_table(request, page):
    all_user_lists = UserInfo.objects.all();
    all_weibo_lists = WeiboInfo.objects.all();
    paginator = Paginator(all_weibo_lists, 11)
    try:
        lists = paginator.page(page)
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)
    return render(request, 'weiboshow.html', { 'lists': lists, 'user_list_count': len(all_user_lists)})