#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from .models import userInfo
from hashlib import sha1
from django.db import connection
import logging
# Create your views here.
logger = logging.getLogger('django_file')
logger1 = logging.getLogger('django_console')
def register(request):
    logger.info('开始渲染并返回注册页面')
    logger1.info('开始渲染并返回注册页面')
    return render(request,'user/register.html')

#接收注册数据
def register_handle(request):
    #接收用户输入
    logger.info('开始注册验证，应该接收post'+request.method)
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    logger.info('验证数据' +uname+uemail+upwd+upwd2)
    #后台判断不能为空
    if not (uname,upwd,upwd2,uemail):
        error_msg = '不能为空'
        return render(request,'user/register.html',{'error':error_msg})
    #判断两次密码是否一致
    if upwd != upwd2:
        error_msg = '两次密码不一致'
        return render(request, 'user/register.html', {'error': error_msg})
    #密码加密
    logger.info('密码加密')
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd3 = s1.hexdigest()
    #创建对象
    logger.info('创建对象')
    user = userInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    logger.info('保存数据'+user.uname+'这是密码'+user.upwd+'邮箱'+user.uemail)
    user.save()
    #注册成功，返回登录界面
    return render(request,'user/login.html')

def register_exist(request):
    #接收get方式传过来的uname，这个get是在js中写的
    uname = request.GET.get('uname')
    #查询这个uname是否存在，如果用get获取，不存在时会返回异常，需要用try except
    count = userInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    logger.info('开始渲染登录页面，会调用cookie')
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'user/login.html',context)

def login_handle(request):
    logger.info('开始登录验证，会生成cookie和session')
    #接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)

    #判断是否为空
    if not (uname and upwd):
        return render(request,'user/login.html',{'error':'用户名和密码均不能为空'})

    #根据用户名查询对象
    users = userInfo.objects.filter(uname=uname)
    print(uname)
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        if s1.hexdigest()==users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            if jizhu != 0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            #pwd错误
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'user/login.html', context)
    else:
        #uname错误
        context = {'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'user/login.html',context)