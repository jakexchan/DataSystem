#-*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.conf import settings
import MySQLdb
import subprocess
import json
import time
# Create your views here.

child = None

def lint_to_db():
    db_arg = settings.DATABASES['default']
    conn = MySQLdb.connect(host=db_arg['HOST'], port=int(db_arg['PORT']), user=db_arg['USER'], passwd=db_arg['PASSWORD'], db=db_arg['NAME'], charset='utf8')
    return conn


def spider_index(request):
    current_user = request.user
    conn = lint_to_db()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""SELECT option_name FROM spider_options
        WHERE user_id = %s """, [current_user.id])

    rows = cursor.fetchall()
    conn.close()
    return render(request, 'spider_index.html', { 'rows': rows })


def create_options(request):
    if request.method == 'POST':
        options_name = request.POST['optionsName']
        keyword = request.POST['keyword']
        delay = request.POST['delay']
        beginPage = request.POST['beginPage']
        endPage = request.POST['endPage']
        t_wm = request.POST['t_wm']
        suhb = request.POST['suhb']
        sub = request.POST['sub']
        gsid_CTandWM = request.POST['gsid_CTandWM']
        user_id = request.POST['user_id']

        #Get time
        t = str(time.time()).replace('.', '')
        user_table = 'user' + t
        weibo_table = 'weibo' + t

        conn = lint_to_db()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        try:
            cursor.execute("""INSERT INTO spider_options(option_name, keyword, delay, begin_page, end_page, user_id, cookies_T_WM, cookies_SUHB, cookies_SUB, cookies_gsid_CTandWM, user_table_name, weibo_table_name)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (options_name, keyword, int(delay), int(beginPage), int(endPage), int(user_id), t_wm, suhb, sub, gsid_CTandWM, user_table, weibo_table))

            cursor.execute("""CREATE TABLE """ + user_table +"""(
                  _id INT NOT NULL AUTO_INCREMENT,
                  u_id VARCHAR(50) NOT NULL UNIQUE,
                  u_name VARCHAR(100),
                  u_weibo_count INT,
                  u_following INT,
                  u_fans INT,
                  u_sex VARCHAR(10),
                  u_region VARCHAR(50),
                  u_birthday VARCHAR(20),
                  u_introduction TEXT,
                  u_tags VARCHAR(100),
                  u_school TEXT,
                  PRIMARY KEY (_id)
                )ENGINE=MyISAM DEFAULT CHARSET=utf8;""")
            cursor.execute("""CREATE TABLE """ + weibo_table + """(
                  _id INT NOT NULL AUTO_INCREMENT,
                  u_id VARCHAR(50) NOT NULL,
                  w_content TEXT,
                  w_type VARCHAR(20),
                  w_day DATE,
                  w_time TIME,
                  w_client VARCHAR(100),
                  PRIMARY KEY (_id)
                )ENGINE=MyISAM DEFAULT CHARSET=utf8;""")

            conn.commit()
            result = True
        except:
            result = False
            conn.rollback()

        conn.close()
        return HttpResponse(result)


def save(request):
    if request.method == 'POST':
        _id = request.POST['id']
        options_name = request.POST['optionsName']
        keyword = request.POST['keyword']
        delay = request.POST['delay']
        beginPage = request.POST['beginPage']
        endPage = request.POST['endPage']
        t_wm = request.POST['t_wm']
        suhb = request.POST['suhb']
        sub = request.POST['sub']
        gsid_CTandWM = request.POST['gsid_CTandWM']
        user_id = request.POST['user_id']

        result = None

        conn = lint_to_db()

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("""UPDATE spider_options s
                SET s.option_name=%s, s.keyword=%s, s.delay=%s, s.begin_page=%s, s.end_page=%s, s.cookies_T_WM=%s, s.cookies_SUHB=%s, s.cookies_SUB=%s, s.cookies_gsid_CTandWM=%s
                WHERE s.id=%s""", (options_name, keyword, int(delay), int(beginPage), int(endPage), t_wm, suhb, sub, gsid_CTandWM, int(_id)))
            result = True
            conn.commit()
        except:
            result = False
            conn.rollback()

        conn.close()
        return HttpResponse(result)


def get_options(request):
    if request.method == 'POST':
        option_name = request.POST['options_name']
        current_user = request.user

        conn = lint_to_db()
        
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM spider_options
            WHERE option_name = %s and user_id = %s""", [option_name, current_user.id])
        result = cursor.fetchone()

        conn.close()
    return HttpResponse(json.dumps(result, ensure_ascii=False))


def crawl(request):
    global child
    if request.method == 'POST':
        _id = request.POST['id']

        conn = lint_to_db()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM spider_options
            WHERE id = %s""", [int(_id)])
        row = cursor.fetchone()
        cursor.close()
        options = {'user_table_name': row['user_table_name'], 'weibo_table_name': row['weibo_table_name'], 'keyword': row['keyword'], 'delay': row['delay'], 'begin_page': row['begin_page'], 'end_page': row['end_page'], 't_wm': row['cookies_T_WM'], 'suhb': row['cookies_SUHB'], 'sub': row['cookies_SUB'], 'gsid_CTandWM': row['cookies_gsid_CTandWM']}
        fw = open('/tmp/options.json', 'w')
        fw.truncate()
        fw.write(json.dumps(options))
        fw.close()
        #cd ../weibo_crawler/weibo_crawler && scrapy crawl weibo
        child = subprocess.Popen('cd ../weibo_crawler/weibo_crawler && scrapy crawl weibo', shell=True)
        child.poll()
    return HttpResponse(child.returncode)


def process_status(request):
    global child
    if request.method == 'POST':
        child.poll()
        return HttpResponse(child.returncode)


def stop_crawl(request):
    global child
    if request.method == 'POST':
        child.kill()
        return HttpResponse(child.returncode)