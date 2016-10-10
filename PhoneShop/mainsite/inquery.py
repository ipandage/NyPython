from .models import *

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

def get_about():
    abouts=About.objects.all()
    return abouts

def get_announcement():
    announcements=Announcement.objects.all()
    return announcements

def get_allow_phone_brands():
    brands=[]
    for item in AllowPhoneBrand.objects.all():
        brands.append(item.brand)
    return brands

def get_allow_tablet_brands():
    brands=[]
    for item in AllowTabletBrand.objects.all():
        brands.append(item.brand)
    return brands


def sql_search(keyword):
    items=[]
    for item in Phone.objects.all():
        if keyword in item.goodsName:
            items.append(item)
    for item in Tablet.objects.all():
        if keyword in item.goodsName:
            items.append(item)
    return items
