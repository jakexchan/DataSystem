"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from system import views as system_views
from system import admin_views as system_admin_views
from django.conf import settings
from django.conf.urls.static import static
from spider import views as spider_views
from system import dataview as data_view


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^spider/$', spider_views.spider_index),
    url(r'^create_options/$', spider_views.create_options, name='create_options'),
    url(r'^get_options/$', spider_views.get_options, name='get_options'),
    url(r'^save/$', spider_views.save, name='save'),
    url(r'^crawl/$', spider_views.crawl, name='crawl'),
    url(r'^process_status/$', spider_views.process_status, name='process_status'),
    url(r'^stop_crawl/$', spider_views.stop_crawl, name='stop_crawl'),
    url(r'^$', system_views.index),
    url(r'^login/$', system_views.login),
    url(r'^registe/$', system_views.registe),
    url(r'^logout/$', system_views.logout),
    url(r'^datashow/user/(\d+)/$', system_views.user_table, name='user_table'),
    url(r'^datashow/weibo/(\d+)/$', system_views.weibo_table, name='weibo_table'),
    url(r'^analysis/', system_views.analysis, name='analysis'),
    url(r'^gender_ratio/$',  system_views.gender_ratio, name='gender_ratio'),
    url(r'^gender_weibo_count/$',  system_views.gender_weibo_count, name='gender_weibo_count'),
    url(r'^gender_follow_count/$',  system_views.gender_follow_count, name='gender_follow_count'),
    url(r'^gender_fans_count/$',  system_views.gender_fans_count, name='gender_fans_count'),
    url(r'^fans_with_weibo/$',  system_views.fans_with_weibo, name='fans_with_weibo'),
    url(r'^age_distribute/$',  system_views.age_distribute, name='age_distribute'),
    url(r'^weibo_compare/$',  system_views.weibo_compare, name='weibo_compare'),
    url(r'^client_compare/$',  system_views.client_compare, name='client_compare'),
    url(r'^day_time/$',  system_views.day_time, name='day_time'),
    url(r'^weibo_update/$',  system_views.weibo_update, name='weibo_update'),
    url(r'^every_day_update/$',  system_views.every_day_update, name='every_day_update'),
    url(r'^high_word/$',  system_views.high_word, name='high_word'),
    url(r'^hot_tags/$',  system_views.hot_tags, name='hot_tags'),
    url(r'^manage/user/$',  system_admin_views.user, name='user'),
    url(r'^gender_result/(.+)/(.+)/$',  data_view.gender, name='gender'),
    url(r'^weibo_count/(.+)/(.+)/(.+)/$',  data_view.weibo_count, name='weibo_count'),
    url(r'^person_info/(.+)/(.+)/$',  data_view.person_info, name='person_info'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
