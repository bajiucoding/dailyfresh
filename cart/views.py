from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import cartInfo
from user import login_auth
from user.models import userInfo
from goods.models import goodsInfo
import logging
# Create your views here.
logger = logging.getLogger('django_console')
@login_auth.auth
def cart(request):
    #为已登录用户返回购物车界面
    user_id = request.session.get('user_id')
    carts = cartInfo.objects.filter(user_id=user_id)
    context = {
        'title':'购物车',
        'page_name':1,
        'carts':carts,
    }
    return render(request,'cart/cart.html',context)
@login_auth.auth
def add(request,gid,count):
    '''
    向购物车中增加商品
    :param request:
    :param gid: 商品id
    :param count: 商品数量
    :return:
    '''
    gid = int(gid)
    count = int(count)
    if gid == 0 and request.is_ajax() and count==0:
        #如果传入的商品id和数量都是0，说明是进入页面时ajax刷新购物车商品数量
        count = cartInfo.objects.filter(user_id=request.session.get('user_id',None)).count()
        return JsonResponse({'count':count})
    #另外一种情况就是向购物车中添加商品
    uid = request.session.get('user_id')
    carts = cartInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts) >= 1:
        #说明购物车中有这项商品，直接加count即可
        cart = carts[0]
        cart.count += count
    else:
        cart = cartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    if request.is_ajax():
        count = cartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'count':count})
    else:
        #转向购物车
        return redirect('/cart/')

#修改商品数量
def edit(request,cid,count):
    try:
        if request.is_ajax():
            goods = cartInfo.objects.get(id=int(cid))
            goods.count = int(count)
            goods.save()
            data = {'ok':1}
    except Exception as e:
        data = {'ok':int(count)}
    return JsonResponse(data)

def delete(request,cid):
    #删除购物车中数据，在cart.html中定义ajax，穿过来的值时cart_id
    try:
        if request.is_ajax():
            goods = cartInfo.objects.get(id=int(cid))
            goods.delete()
            data = {'ok':1}
    except Exception as e:
        data = {'ok':0,'e':e}
        return JsonResponse(data)


def place_order(request,url_id,*args):
    #订单界面对应方法，从detail界面直接购买或者购物车结算按钮到达。需要返回数据包括用户购物地址，商品列表
    logger.info('接收到参数'+str(url_id)+str(args)+str(args[0]))
    uid = request.session['user_id']
    logger.info('当前用户'+str(uid))
    users = userInfo.objects.filter(id=uid)
    address = users[0].uaddress
    people = users[0].ustockAddress
    phone = users[0].uphone
    if int(url_id) == 1:
        #说明是从detail页面过来的，就一件商品.未经过购物车
        logger.info('直接从detail界面购买了，购买人是'+people)
        gid = args[0]
        goods = goodsInfo.objects.filter(id=gid)[0]
        logger.info('购买货物：'+goods.gtitle)
        context = {
            'url_id': url_id,
            'user':address+' '+people+' '+phone,
            'goods':goods,
        }
        return render(request,'cart/place_order.html',context)
    if int(url_id) == 2:
        #从购物车界面过来，args参数是购物车id
        logger.info('购物车跳转')
        cart = cartInfo.objects.filter(user_id=args)
        context = {
            'url_id':url_id,
            'user':address+' '+people+' '+phone,
            'carts':cart,
        }
        return render(request,'cart/place_order.html',context)
