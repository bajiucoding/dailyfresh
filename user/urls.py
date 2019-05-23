#coding=utf-8
'''
*************************
file:       allproject urls
author:     gongyi
date:       2019/5/13 15:29
****************************
change activity:
            2019/5/13 15:29
'''
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/',views.register,name='register_url_name'),
    url(r'^register_handle/$',views.register_handle),
    url(r'^login/',views.login,name='login_url_name'),
    url(r'^login_handle/$',views.login_handle),
    url(r'logout',views.logout,name='logout_url_name'),
    url(r'info',views.info,name='info_url_name'),
    url(r'order',views.order,name='order_url_name'),
    url(r'site',views.site,name='site_url_name')
]