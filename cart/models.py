from django.db import models

# Create your models here.

class cartInfo(models.Model):
    user = models.ForeignKey('user.userInfo',on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.goodsInfo',on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name = '购物车商品信息'
        verbose_name_plural = '购物车商品信息'
