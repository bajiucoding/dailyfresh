#coding=utf-8
'''
*************************
file:       allproject search_indexes
author:     gongyi
date:       2019/5/20 17:37
****************************
change activity:
            2019/5/20 17:37
'''
from haystack import indexes
from .models import goodsInfo

class GoodInfoIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return goodsInfo

    def index_queryset(self,using=None):
        return self.get_model().objects.all()