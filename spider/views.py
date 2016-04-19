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


def save(request):
    if request.method == 'POST':
        _id = request.POST['_id']
        options_name = request.POST['optionsName']
        url = request.POST['url']
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
        cursor.execute("""SELECT * FROM spider_options
            WHERE _id = %s""", [int(_id)])
        row = cursor.fetchone()
        print row
        import pdb; pdb.set_trace()
        if row is None:      
            try:
                cursor.execute("""INSERT INTO spider_options(option_name, url, keyword, delay, begin_page, end_page, cookies_T_WM, cookies_SUHB, cookies_SUB, cookies_gsid_CTandWM, user_id) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (options_name, url, keyword, int(delay), int(beginPage), int(endPage), t_wm, suhb, sub, gsid_CTandWM, int(user_id)))
                result = True
                conn.commit()
            except:
                result = False
                conn.rollback()
        else:
            try:
                cursor.execute("""UPDATE spider_options s
                    SET s.option_name=%s, s.url=%s, s.keyword=%s, s.delay=%s, s.begin_page=%s, s.end_page=%s, s.cookies_T_WM=%s, s.cookies_SUHB=%s, s.cookies_SUB=%s, s.cookies_gsid_CTandWM=%s
                    WHERE s._id=%s""", (options_name, url, keyword, int(delay), int(beginPage), int(endPage), t_wm, suhb, sub, gsid_CTandWM, _id))
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
        url = request.POST['url']
        keyword = request.POST['keyword']
        delay = request.POST['delay']
        begin_page = request.POST['beginPage']
        end_page = request.POST['endPage']
        t_wm = request.POST['t_wm']
        suhb = request.POST['suhb']
        sub = request.POST['sub']
        gsid_CTandWM = request.POST['gsid_CTandWM']

        options = {'url': url, 'keyword': keyword, 'delay': delay, 'begin_page': begin_page, 'end_page': end_page, 't_wm': t_wm, 'suhb': suhb, 'sub': sub, 'gsid_CTandWM': gsid_CTandWM}
        fw = open('/tmp/options.json', 'w')
        fw.truncate()
        fw.write(json.dumps(options))
        fw.close()
        #cd ../weibo_crawler/weibo_crawler && scrapy crawl weibo
        child = subprocess.Popen('ping -c4 www.baidu.com', shell=True)
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