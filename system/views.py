#-*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import forms
import MySQLdb
import pandas as pd
import numpy
import jieba
import sys
import jieba.analyse
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
                if username == 'admin':
                    return HttpResponseRedirect('/manage/user/')
                else:
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
        cursor = connection.cursor()
        cursor.execute("""SELECT id
            FROM auth_user
            WHERE username=%s""", [username])
        row = cursor.fetchone()
        cursor.execute("""INSERT INTO user_profile(profile, user_id)
            VALUES(%s,%s)""", ['普通用户', row[0]])
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
    conn.close()
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
    conn.close()
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
    conn.close()
    return HttpResponse(json.dumps(result, ensure_ascii=False))


@login_required
def age_distribute(request):
    conn = link_to_db()
    # cursor = conn.cursor()
    # try:
    #     cursor.execute(""" SELECT (YEAR(CURDATE()) - YEAR(u_birthday))age from user_info having age != '' order by age """)
    #     #cursor.execute("""select * from user_info""")
    #     rows = cursor.fetchall()
    #     print rows
    # except:
    #     print 'error'
    df = pd.read_sql("select * from user_info", conn)


    return HttpResponse(json.dumps(rows, ensure_ascii=False))


def top_six_client(df):
    client = df.groupby(['w_client']).size().sort_values(ascending=False)
    top_six = client[:6]
    result = dict()
    for i, value in enumerate(top_six):
        result[top_six.index[i]] = str(value)
    return result

@login_required
def weibo_compare(request):
    conn = link_to_db()
    df_original = pd.read_sql("select * from weibo_info where w_type='原创'", conn)
    df_transmit = pd.read_sql("select * from weibo_info where w_type='转发'", conn)

    original_count = len(df_original)
    transmit_count = len(df_transmit)

    original_client = top_six_client(df_original)
    transmit_client = top_six_client(df_transmit)
    result = [{u'原创':[original_count, original_client]}, {u'转发':[transmit_count, transmit_client]}]
    conn.close()
    return HttpResponse(json.dumps(result, ensure_ascii=False))

@login_required
def client_compare(request):
    conn = link_to_db()
    df = pd.read_sql("select * from weibo_info", conn)
    df_client = df.groupby(['w_client']).size().sort_values(ascending=False)
    df_client_top_ten = df_client[:10]
    count = 0
    result = dict()
    for i, value in enumerate(df_client_top_ten):
        if df_client_top_ten.index[i] != '':
            count += value
            result[df_client_top_ten.index[i]] = str(value)
    result[u'总数'] = str(count)
    conn.close()
    return HttpResponse(json.dumps(result, ensure_ascii=False))


@login_required
def day_time(request):
    conn = link_to_db()
    df = pd.read_sql("select * from weibo_info", conn)
    day_time = df.loc[:, ['w_day', 'w_time']]
    result = []
    for i in range(len(day_time)):
        result.append([ str(day_time['w_day'][i]), str(day_time['w_time'][i]).split(' ')[2] ])
    conn.close()
    return HttpResponse(json.dumps(result, ensure_ascii=False))

def weibo_day_update(df):
    df_dt = pd.to_datetime(df['w_day'])
    days = {0:'周一',1:'周二',2:'周三',3:'周四',4:'周五',5:'周六',6:'周日'}
    new_arr = []
    for i in df_dt:
        new_arr.append(days[i.weekday()])
    df['week'] = new_arr
    grouped = df.groupby(by=['week']).size()
    result = dict()
    for i, value in enumerate(grouped):
        result[grouped.index[i]] = str(value)
    return result

@login_required
def weibo_update(request):
    conn = link_to_db()
    df_sum = pd.read_sql("select * from weibo_info", conn)
    df_original = pd.read_sql("select * from weibo_info where w_type='原创'", conn)
    df_transmit = pd.read_sql("select * from weibo_info where w_type='转发'", conn)

    sum_update = weibo_day_update(df_sum)
    original_update = weibo_day_update(df_original)
    df_transmit = weibo_day_update(df_transmit)

    result = [{'总体': sum_update}, {'原创': original_update}, {'转发': df_transmit}]
    conn.close()
    return HttpResponse(json.dumps(result, ensure_ascii=False))


@login_required
def every_day_update(request):
    conn = link_to_db()
    df = pd.read_sql('select * from weibo_info', conn)
    df_day = df.groupby(by=['w_day']).size()
    obj = dict()
    result = []
    for i, value in enumerate(df_day):
        obj = dict()
        obj[str(df_day.index[i])] = str(value)
        result.append(obj)
        del obj
    conn.close()
    return HttpResponse(json.dumps(result, ensure_ascii=False))


@login_required
def high_word(request):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    conn = link_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT w_content FROM weibo_info")
    rows = cursor.fetchall()
    fw = open('weibo.txt', 'w')
    fw.truncate()
    for row in rows:
        fw.write(row[0])
        fw.write('\n')
    fw.close()
    content = open('weibo.txt', 'r').read()
    # tags = jieba.analyse.extract_tags(content, topK=10)
    words = [ word for word in jieba.cut(content, cut_all=True) if len(word) >= 2 ]
    result = dict()
    for word in words:
        if result.get(word) is None:
            result[word] = 1
        else:
            result[word] += 1
    result = sorted(result.iteritems(), key=lambda d:d[1], reverse=True)
    return HttpResponse(json.dumps(result[:10], ensure_ascii=False))