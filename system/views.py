#-*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt
import forms
import MySQLdb
import pandas as pd
import numpy
from django.conf import settings
from models import UserInfo, WeiboInfo
import json
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


@login_required
def analysis(request):
    return render(request, 'analysis.html')


def link_to_db():
    db_arg = settings.DATABASES['default']
    conn = MySQLdb.connect(host=db_arg['HOST'], port=int(db_arg['PORT']), user=db_arg['USER'], passwd=db_arg['PASSWORD'], db=db_arg['NAME'], charset='utf8')
    return conn


@login_required
def gender_ratio(request):
    conn = link_to_db()
    df = pd.read_sql('select * from user_info', conn)
    gender = df.groupby(['u_sex']).size()
    result = dict()
    for i, value in enumerate(gender):
        result[gender.index[i]] = value
    conn.close()
    return HttpResponse(json.dumps(result, ensure_ascii=False))


def weibo_layered(df):
    labels = ['0-100', '100-1000', '1000-2000', '2000-5000', '5000-10000', '10000以上']
    bins = [min(df.u_weibo_count)-1, 100, 1000, 2000, 5000, 10000, max(df.u_weibo_count)+1]
    df['layered'] =  pd.cut(df.u_weibo_count, bins, labels=labels)
    layered = df.groupby(by=['layered']).size()
    result = dict()
    for i, value in enumerate(layered):
        result[layered.index[i]] = value
    return result


@login_required
def gender_weibo_count(request):
    conn = link_to_db()
    df_male = pd.read_sql("select * from user_info where u_sex='男'", conn)
    df_female = pd.read_sql("select * from user_info where u_sex='女'", conn)

    male_result = weibo_layered(df_male)
    female_result = weibo_layered(df_female)

    result = [{'男': male_result}, {'女': female_result}]
    return HttpResponse(json.dumps(result, ensure_ascii=False))


def follow_layered(df):
    labels = ['0-200', '200-400', '400-600', '600-800', '800-1000', '1000以上']
    bins = [min(df.u_following)-1, 200, 400, 600, 800, 1000, max(df.u_following)+1]
    df['layered'] =  pd.cut(df.u_following, bins, labels=labels)
    layered = df.groupby(by=['layered']).size()
    result = dict()
    for i, value in enumerate(layered):
        result[layered.index[i]] = value
    return result


@login_required
def gender_follow_count(request):
    conn = link_to_db()
    df_male = pd.read_sql("select * from user_info where u_sex='男'", conn)
    df_female = pd.read_sql("select * from user_info where u_sex='女'", conn)

    male_result = follow_layered(df_male)
    female_result = follow_layered(df_female)
    
    result = [{'男': male_result}, {'女': female_result}]
    return HttpResponse(json.dumps(result, ensure_ascii=False))


def fans_layered(df):
    labels = ['0-500', '500-1000', '1000-3000', '3000-5000', '5000-10000', '10000以上']
    bins = [min(df.u_fans)-1, 500, 1000, 3000, 5000, 10000, max(df.u_fans)+1]
    df['layered'] =  pd.cut(df.u_fans, bins, labels=labels)
    layered = df.groupby(by=['layered']).size()
    result = dict()
    for i, value in enumerate(layered):
        result[layered.index[i]] = value
    return result


@login_required
def gender_fans_count(request):
    conn = link_to_db()
    df_male = pd.read_sql("select * from user_info where u_sex='男'", conn)
    df_female = pd.read_sql("select * from user_info where u_sex='女'", conn)

    male_result = fans_layered(df_male)
    female_result = fans_layered(df_female)
    
    result = [{'男': male_result}, {'女': female_result}]
    return HttpResponse(json.dumps(result, ensure_ascii=False))