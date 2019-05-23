from django.db import models

# Create your models here.

class userInfo(models.Model):
    '''用户信息模型'''
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=80)
    uemail = models.CharField(max_length=30)
    #收货人  名字写错了
    ustockAddress = models.CharField(max_length=30,default='')
    #详细地址
    uaddress = models.CharField(max_length=100,default='')
    #邮编
    uemailAddress = models.CharField(max_length=6,default='')
    #手机号
    uphone = models.CharField(max_length=11,default='')