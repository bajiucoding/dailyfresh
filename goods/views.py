from django.shortcuts import render
from .models import typeInfo,goodsInfo
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging
logger = logging.getLogger('django_console')
# Create your views here.


def index(request):
    '''
    主界面
    :param request:
    :return:
    '''
    logger.info('当前用户' + str(request.session.get('user_name')) + '进入商城主界面界面')
    typelist = typeInfo.objects.all()                   #获得商品种类
    type0 = typelist[0].type_title.order_by('-id')[0:4]  #根据商品种类获取对应货物按id逆序的前4条数据
    type01 = typelist[0].type_title.order_by('gclick')[0:4]  #获取点击量最多的4条商品信息
    type1 = typelist[1].type_title.order_by('-id')[0:4]  #
    type11 = typelist[1].type_title.order_by('gclick')[0:4]
    type2 = typelist[2].type_title.order_by('-id')[0:4]  #
    type21 = typelist[2].type_title.order_by('gclick')[0:4]
    type3 = typelist[3].type_title.order_by('-id')[0:4]  #
    type31 = typelist[3].type_title.order_by('gclick')[0:4]
    type4 = typelist[4].type_title.order_by('-id')[0:4]  #
    type41 = typelist[4].type_title.order_by('gclick')[0:4]
    type5 = typelist[5].type_title.order_by('-id')[0:4]  #
    type51 = typelist[5].type_title.order_by('gclick')[0:4]
    context = {
        'title':'首页',
        'type0':type0,'type01':type01,
        'type1':type1,'type11':type11,
        'type2':type2,'type21':type21,
        'type3':type3,'type31':type31,
        'type4':type4,'type41':type41,
        'type5':type5,'type51':type51,
    }
    return render(request,'goods/index.html',context)

def list(request,type_id,page_index,type_sort):
    '''
    商品列表界面
    :param request:
    :param type_id:商品类型id
    :param page_index:商品所在页
    :param type_sort:排序规则
    :return:
    '''
    logger.info('当前用户' + str(request.session.get('user_name')) + '进入详细列表界面')
    typeinfo = typeInfo.objects.get(id=int(type_id))
    news = typeinfo.type_title.order_by('-id')[0:2]   #取该类型最新的两个
    if type_sort == '1': #按照最新排序
        good_list = goodsInfo.objects.filter(gtype_id=int(type_id)).order_by('-id')
    elif type_sort == '2':  #按价格
        good_list = goodsInfo.objects.filter(gtype_id=int(type_id)).order_by('-gprice')
    elif type_sort == '3':  #按点击量
        good_list = goodsInfo.objects.filter(gtype_id=int(type_id)).order_by('-gclick')
    paginator = Paginator(good_list,10)    #分页，每页有10个元素
    page = paginator.page(int(page_index))  #获得当前页的元素列表
    context = {
        'title':typeinfo.ttitle,    #当前分类名称
        'page':page,                #排序后的当前页列表
        'typeinfo':typeinfo,         #当前分类的信息
        'news':news,                #新品推荐列表
        'g_sort':type_sort,           #代表排序规则的数字
        'paginator':paginator,      #分页
    }
    return render(request,'goods/list.html',context)

def detail(request,id):
    '''
    商品详情界面
    :param request:
    :return:
    '''
    logger.info('当前用户' + str(request.session.get('user_name')) + '进入详细信息界面')
    goods = goodsInfo.objects.get(id=int(id))
    goods.gclick = goods.gclick + 1
    goods.save()
    news = goods.gtype.type_title.order_by('-id')[0:2]
    context = {
        'title':goods.gtype.ttitle,
        'goods':goods,
        'news':news,
        'id':id,
    }
    return render(request,'goods/detail.html',context)

    #缓存记录用户的最近浏览历史
    if request.session.has_key('user_id'):   #如果登陆了
        logger.info('当前用户' + request.session.get('user_name') + '正在记录他的浏览历史')
        key = str(request.session.get('user_id'))
        goods_ids = request.session.get(key,'')
        goods_id = str(goods.id)  #这是当前浏览的商品id
        if goods_ids != '':
            #当前用户有浏览记录
            if goods_id in goods_ids:  #当前商品在浏览记录中存在
                goods_ids.remove(goods_id)  #删除存在的第一个记录，只会存在这一个
                goods_ids.insert(0,goods_id)   #在首部加入一个
            if len(goods_ids) > 5:  #如果超过5个就删除最后一个
                goods_ids.pop()
        else:
            goods_ids = []
            goods_ids.append(goods_id)
        request.session[key] = goods_ids
    return response

from haystack.views import SearchView
from dailyFresh.settings import HAYSTACK_SEARCH_RESULTS_PER_PAGE

class MySearchView(SearchView):
    def build_page(self):
        '''
        重写分页
        :return:
        '''
        logger.info('开始搜索了')
        context = super(MySearchView, self).extra_context()  #继承自带的context
        try:
            page_no = int(self.request.GET.get('page',1))
        except Exception:
            return HttpResponse('页面数不合法')

        if page_no < 1:
            return HttpResponse('页面数应该大于等于1')
        a = []
        for i in self.results:
            a.append(i.object)
        paginator = Paginator(a,HAYSTACK_SEARCH_RESULTS_PER_PAGE)
        page = paginator.page(page_no)
        return (paginator,page)

    def extra_context(self):
        context = super(MySearchView, self).extra_context()  #继承自带的context
        context['title'] = '搜索'
        return context

