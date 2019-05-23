#coding=utf-8
'''
*************************
file:       allproject urls
author:     gongyi
date:       2019/5/19 17:23
****************************
change activity:
            2019/5/19 17:23
'''
from django.conf.urls import url
from .views import index,list,detail,MySearchView

urlpatterns = [
    url(r'^$',index,name='url_index_name'),
    url(r'detail/(\d+)/$',detail,name='url_detail_name'),
    url(r'^list(\d+)_(\d+)_(\d+)/$',list,name='url_list_name'),
    url(r'^search/$',MySearchView),
]