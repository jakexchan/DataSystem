from __future__ import unicode_literals

from django.db import models

# Create your models here.
class SpiderOptions(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)
    option_name = models.CharField(max_length=255)
    delay = models.IntegerField(blank=True)
    cookies_T_WM = models.CharField(max_length=255)
    cookies_SUHB = models.CharField(max_length=255)
    cookies_SUB = models.CharField(max_length=255)
    cookies_gsid_CTandWM = models.CharField(max_length=255)
    strat_url = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    strat_page = models.IntegerField(blank=True)
    stop_page = models.IntegerField(blank=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spider_options'