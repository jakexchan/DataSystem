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

def gender(request):
    if request.method == 'POST':
        project_name = request.POST['project_name']
        gender_value = request.POST['gender_value']
        conn = link_to_db()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT user_table_name FROM spider_options
            WHERE id = %s""", [project_name])
        table_name = cursor.fetchone()
        cursor.execute("""SELECT * FROM """ + table_name['user_table_name'] + """
            WHERE u_sex = %s""", [gender_value])
        result = cursor.fetchall()
        print result
        conn.close()
    return HttpResponse(json.dumps(result, ensure_ascii=False))

