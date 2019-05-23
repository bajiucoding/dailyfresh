#coding=utf-8
'''
*************************
file:       allproject urls
author:     gongyi
date:       2019/5/21 21:13
****************************
change activity:
            2019/5/21 21:13
'''
from django.conf.urls import url
from .views import cart,add,edit,delete,place_order

urlpatterns = [
    url(r'^$',cart,name='url_cart_name'),
    url(r'^add(\d+)_(\d+)/$',add),
    url(r'^edit(\d+)_(\d+)/$',edit),
    url(r'^delete(\d+)/$',delete),
    url(r'^place_order/(\d+)/(\d+)/$',place_order),
]