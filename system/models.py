# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.contrib.auth.models import UserManager
from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class UserInfo(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    u_id = models.CharField(unique=True, max_length=50)
    u_name = models.CharField(max_length=100, blank=True, null=True)
    u_weibo_count = models.IntegerField(blank=True, null=True)
    u_following = models.IntegerField(blank=True, null=True)
    u_fans = models.IntegerField(blank=True, null=True)
    u_sex = models.CharField(max_length=10, blank=True, null=True)
    u_region = models.CharField(max_length=50, blank=True, null=True)
    u_birthday = models.CharField(max_length=20, blank=True, null=True)
    u_introduction = models.TextField(blank=True, null=True)
    u_tags = models.CharField(max_length=100, blank=True, null=True)
    u_school = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'


class WeiboInfo(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    u_id = models.CharField(max_length=50)
    w_content = models.TextField(blank=True, null=True)
    w_type = models.CharField(max_length=20, blank=True, null=True)
    w_day = models.DateField(blank=True, null=True)
    w_time = models.TimeField(blank=True, null=True)
    w_client = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weibo_info'

            