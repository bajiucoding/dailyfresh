from django.contrib import admin
from .models import typeInfo,goodsInfo
# Register your models here.

class typeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle']

class goodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 100         #每页中放置的数据量
    list_display = ['id','gtitle','gprice','gunit','gclick','gstock','gcontent','gtype']

admin.site.register(typeInfo,typeInfoAdmin)
admin.site.register(goodsInfo,goodsInfoAdmin)