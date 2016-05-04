#-*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import connection
import forms
import MySQLdb
import json

def link_to_db():
    db_arg = settings.DATABASES['default']
    conn = MySQLdb.connect(host=db_arg['HOST'], port=int(db_arg['PORT']), user=db_arg['USER'], passwd=db_arg['PASSWORD'], db=db_arg['NAME'], charset='utf8')
    return conn

def gender(request, project_name, gender_value):
    if request.method == 'GET':
        conn = link_to_db()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT user_table_name FROM spider_options
            WHERE id = %s""", [project_name])
        table_name = cursor.fetchone()
        cursor.execute("""SELECT * FROM """ + table_name['user_table_name'] + """
            WHERE u_sex = %s""", [gender_value])
        result = cursor.fetchall()
        conn.close()
    return render(request, 'dataview.html', { 'result': result })

def weibo_count(request, project_name, gender_value,number):
    if request.method == 'GET':
        num = number.split('-')
        min_num = num[0]
        max_num = num[1]
        conn = link_to_db()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT user_table_name FROM spider_options
            WHERE id = %s""", [project_name])
        table_name = cursor.fetchone()
        cursor.execute("""SELECT * FROM """ + table_name['user_table_name'] + """
            WHERE u_sex = %s AND u_weibo_count > %s AND u_weibo_count < %s""", [gender_value, min_num, max_num])
        result = cursor.fetchall()
        conn.close()
    return render(request, 'dataview.html', { 'result': result })