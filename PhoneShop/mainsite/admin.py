from django.contrib import admin
from .models import *
# Register your models here.

class PhoneAdmin(admin.ModelAdmin):
    list_display = ('brand','goodsNum','goodsName','price','pub_date',)

class PriceAdmin(admin.ModelAdmin):
    list_display = ('price_from','price_to','price_add',)

class TabletAdmin(admin.ModelAdmin):
    list_display = ('brand','goodsNum','goodsName','price','pub_date',)

class SmartItemAdmin(admin.ModelAdmin):
    list_display = ('brand','goodsNum','goodsName','price','pub_date',)

class AboutAdmin(admin.ModelAdmin):
    list_display = ('infor','pub_date',)

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('infor','pub_date',)

class AllowPhoneBrandAdmin(admin.ModelAdmin):
    list_display = ('brand','pub_date',)

class AllowTabletBrandAdmin(admin.ModelAdmin):
    list_display = ('brand','pub_date',)


admin.site.register(Phone,PhoneAdmin)
admin.site.register(Price,PriceAdmin)
admin.site.register(Tablet,TabletAdmin)
admin.site.register(SmartItem,SmartItemAdmin)
admin.site.register(Announcement,AnnouncementAdmin)
admin.site.register(About,AboutAdmin)
admin.site.register(AllowPhoneBrand,AllowPhoneBrandAdmin)
admin.site.register(AllowTabletBrand,AllowTabletBrandAdmin)
