from django.contrib import admin
from .models import Phone,Price,Tablet
# Register your models here.

class PhoneAdmin(admin.ModelAdmin):
    list_display = ('brand','goodsNum','goodsName','price','pub_date',)

class PriceAdmin(admin.ModelAdmin):
    list_display = ('price_from','price_to','price_add',)

class TabletAdmin(admin.ModelAdmin):
    list_display = ('brand','goodsNum','goodsName','price','pub_date',)

admin.site.register(Phone,PhoneAdmin)
admin.site.register(Price,PriceAdmin)
admin.site.register(Tablet,TabletAdmin)
