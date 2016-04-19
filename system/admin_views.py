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

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def user(request):
    cursor = connection.cursor()
    cursor.execute("""SELECT u.id, u.username, u.email,u.date_joined, u.last_login, p.sex, p.profile 
        FROM auth_user AS u, user_profile AS p
        WHERE u.id = p.user_id AND u.username != 'admin'""")
    rows = dictfetchall(cursor)
    print rows
    return render(request, 'user.html', { 'rows': rows })