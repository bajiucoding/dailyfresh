#coding=utf-8
'''
*************************
file:       allproject login_auth
author:     gongyi
date:       2019/5/20 19:43
****************************
change activity:
            2019/5/20 19:43
'''
#装饰器登录验证
from django.http import HttpResponseRedirect

def auth(func):
    def login_auth(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            #说明用户已登录，直接返回继续执行原函数
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            #未登录时，就返回登录界面，同时将用户请求的页面存在cookie里，url字段。在登录那儿直接跳转到url
            red.set_cookie('url',request.get_full_path())
            return red

    return login_auth