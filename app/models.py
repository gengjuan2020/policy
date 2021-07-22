# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class AppDevice(models.Model):
    dev_name = models.CharField(max_length=100,null=False)
    dev_type = models.ForeignKey('dev_type',to_field="d_type",on_delete=models.CASCADE)
    dev_ip = models.CharField(max_length=100,null=False,unique=True)
    dev_user = models.CharField(max_length=100,null=False)
    dev_password = models.CharField(max_length=100,null=False)
    dev_mgt= models.ForeignKey('mgt_type',to_field="type_sb",on_delete=models.CASCADE)
    dev_code=models.ForeignKey('Code_name',to_field="name",on_delete=models.CASCADE,null=True)
    dev_time = models.DateTimeField(auto_now=True)



class devgroup(models.Model):
    group_name=models.ForeignKey("devgroup_name", to_field="devgroup_name", on_delete=models.CASCADE)
    dev_ip = models.ForeignKey("AppDevice",to_field='dev_ip',on_delete=models.CASCADE)
    group_time = models.DateTimeField(auto_now=True)


class devgroup_name(models.Model):

    devgroup_name=models.CharField(max_length=100,null=False,unique=True)
    devgroup_time = models.DateTimeField(auto_now=True)


class dev_type(models.Model):

    d_type=models.CharField(max_length=100,null=False,unique=True)
    d_time = models.DateTimeField(auto_now=True)

class mgt_type(models.Model):

    type_sb=models.CharField(max_length=100,null=False,unique=True)

class attlog(models.Model):

    log_name=models.CharField(max_length=100,null=False)
    log_dev=models.CharField(max_length=100,null=False)
    log_area=models.CharField(max_length=100,null=False)
    log_srcip=models.CharField(max_length=100,null=False)
    log_dstip=models.CharField(max_length=100,null=False)
    log_payload=models.CharField(max_length=3000,null=False)
    log_time = models.DateTimeField(auto_now=True)
    log_status= models.CharField(max_length=100,null=False)

class Analysis(models.Model):

    log_name=models.CharField(max_length=100,null=False)
    log_dev=models.CharField(max_length=100,null=False)
    log_area=models.CharField(max_length=100,null=False)
    log_srcip=models.CharField(max_length=100,null=False)
    log_dstip=models.CharField(max_length=100,null=False)
    log_payload=models.CharField(max_length=3000,null=False)
    log_time = models.DateTimeField(auto_now=True)
    log_fenxi=models.CharField(max_length=3000,null=False)
    log_status= models.CharField(max_length=100,null=False)
class Fdjl(models.Model):
    log_ip = models.CharField(max_length=100)
    log_time = models.DateTimeField(auto_now=True)
class Code_name(models.Model):
     name= models.CharField(max_length=100,unique=True)
     neirong=models.CharField(max_length=3000,null=True)
     time= models.DateTimeField(auto_now=True)