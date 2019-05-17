from django.db import models

# Create your models here.

class userInfo(models.Model):
    '''用户信息模型'''
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=80)
    uemail = models.CharField(max_length=30)
    ustockAddress = models.CharField(max_length=30,default='')
    uaddress = models.CharField(max_length=100,default='')
    uemailAddress = models.CharField(max_length=6,default='')
    uphone = models.CharField(max_length=11,default='')