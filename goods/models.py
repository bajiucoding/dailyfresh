from django.db import models
from tinymce.models import HTMLField
# Create your models here.

#商品分类模型
class typeInfo(models.Model):
    ttitle = models.CharField('商品分类',max_length=20)
    isDelete = models.BooleanField('逻辑删除',default=False)

    def __str__(self):
        return self.ttitle

    class Meta:
        verbose_name = '商品类型'
        verbose_name_plural = '商品类型'

# 商品信息
class goodsInfo(models.Model):
    gtitle = models.CharField('商品名称',max_length=20)
    gpic = models.ImageField('商品图片',upload_to='goods',null=True,blank=True)
    gprice = models.DecimalField('商品价格',max_digits=7,decimal_places=2)  #商品价格
    gunit = models.CharField('商品单位',max_length=20,default='500g')  #商品单位
    gclick = models.IntegerField('点击量',default=0)  #商品点击量
    isDelete = models.BooleanField('逻辑删除',default=False)
    gintro = models.CharField('简介',max_length=200)
    gstock = models.IntegerField('库存')
    gcontent = HTMLField('详细介绍')
    gtype = models.ForeignKey(typeInfo,related_name='type_title',verbose_name='所属分类',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'