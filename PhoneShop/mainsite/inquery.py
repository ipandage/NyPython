from .models import Phone,Price,Tablet
from  .inquery import *

def get_tablet_brands():
    brands=[]
    for item in Tablet.objects.all():
        if item.brand in brands:
            continue
        brands.append(item.brand)
    return brands

def get_phone_brands():
    brands=[]
    for item in Phone.objects.all():
        if item.brand in brands:
            continue
        brands.append(item.brand)
    return brands

def get_phones(brand=''):
    if brand=='':
        return Phone.objects.all()
    result=Phone.objects.filter(brand=brand)
    return result

def get_tablets(brand=''):
    if brand=='':
        return Tablet.objects.all()
    result=Tablet.objects.filter(brand=brand)
    return result

def get_item(goodsNum):
    item=Phone.objects.filter(goodsNum=goodsNum)
    if len(item)==0:
        item=Tablet.objects.filter(goodsNum=goodsNum)
    if len(item)==0:
        return False
    return item[0]

def get_priceadd():
    prices=Price.objects.all()
    return prices
