from .inquery import *
from django.shortcuts import render
from django.http import HttpResponse
from django.http  import HttpResponseRedirect
from django.template.loader import render_to_string
import time
# Create your views here.

def index(request):
    phone_brands=[]
    tablet_brands=[]
    allow_phones=get_allow_phone_brands()
    allow_tablets=get_allow_tablet_brands()
    for item in get_phone_brands():
        if item in allow_phones:
            phone_brands.append(item)

    all_phones=get_phones()
    date_today=int(time.strftime("%Y%m%d"))
    phones=[]
    need_phones={}
    for product in all_phones:
        update_date=int(product.pub_date.split(' ')[0].replace('-',''))
        if date_today-update_date>=2:
            continue
        if product.brand not in phone_brands:
            continue
        item={}
        item['goodsName']=product.goodsName
        item['brand']=product.brand
        item['goodsNum']=product.goodsNum
        if product.brand in need_phones:
            need_phones[product.brand].append(item)
        else:
            need_phones[product.brand]=[item]
    for brand in phone_brands:
        try:
            items=need_phones[brand]
        except:
            continue
        phones.append({'name':brand,'items':items})

    for item in get_tablet_brands():
        if item in allow_tablets:
            tablet_brands.append(item)

    all_tablets=get_tablets()
    date_today=int(time.strftime("%Y%m%d"))
    need_tablets={}
    tablets=[]
    for product in all_tablets:
        update_date=int(str(product.pub_date).split(' ')[0].replace('-',''))
        if date_today-update_date>=2:
            continue
        if product.brand not in tablet_brands:
            continue
        item={}
        item['goodsName']=product.goodsName
        item['brand']=product.brand
        item['goodsNum']=product.goodsNum
        if product.brand in need_tablets:
            need_tablets[product.brand].append(item)
        else:
            need_tablets[product.brand]=[item]

    for brand in tablet_brands:
        try:
            items=need_tablets[brand]
        except:
            continue
        tablets.append({'name':brand,'items':items})

    announcements=[]
    for item in get_announcement():
        announcements.append(item.infor)

    all_smartitems=get_smart_items()
    date_today=int(time.strftime("%Y%m%d"))
    smart_items={}
    for product in all_smartitems:
        update_date=int(str(product.pub_date).split(' ')[0].replace('-',''))
        if date_today-update_date>=2:
            continue
        item={}
        item['goodsName']=product.goodsName
        item['brand']=product.brand
        item['goodsNum']=product.goodsNum
        if product.brand in smart_items:
            smart_items[product.brand].append(item)
        else:
            smart_items[product.brand]=[item]
    smart_items_list=[]
    for key in smart_items:
        item={'name':key,'items':smart_items[key]}
        smart_items_list.append(item)
    return render(request,'index.html',{'smartitems':smart_items_list,'tablets':tablets,'phones':phones,'phone_brands':phone_brands,'tablet_brands':tablet_brands,'announcements':announcements})

def smartphone(request):
    phone_brands=[]
    tablet_brands=[]
    allow_phones=get_allow_phone_brands()
    allow_tablets=get_allow_tablet_brands()
    for item in get_phone_brands():
        if item in allow_phones:
            phone_brands.append(item)
    for item in get_tablet_brands():
        if item in allow_tablets:
            tablet_brands.append(item)
    try:
        brand=request.GET['brand']
    except:
        brand=''
    results=get_phones(brand)
    items=[]
    prices=get_priceadd()
    date_today=int(time.strftime("%Y%m%d"))
    for product in results:
        update_date=int(str(product.pub_date).split(' ')[0].replace('-',''))
        if date_today-update_date>=2:
            continue
        item={}
        product_price=float(product.price)
        for price in prices:
            price_from=price.price_from
            price_to=price.price_to
            price_add=price.price_add
            if product_price>=price_from and product_price<price_to:
                product_price+=price_add
                break
        item['price']=product_price
        item['goodsName']=product.goodsName
        item['brand']=product.brand
        item['goodsNum']=product.goodsNum
        items.append(item)
    return render(request,'items.html',{'brand':brand,'items':items,'phone_brands':phone_brands,'tablet_brands':tablet_brands})

def tablets(request):
    phone_brands=[]
    tablet_brands=[]
    allow_phones=get_allow_phone_brands()
    allow_tablets=get_allow_tablet_brands()
    for item in get_phone_brands():
        if item in allow_phones:
            phone_brands.append(item)
    for item in get_tablet_brands():
        if item in allow_tablets:
            tablet_brands.append(item)
    try:
        brand=request.GET['brand']
    except:
        brand=''
    results=get_tablets(brand)
    items=[]
    prices=get_priceadd()
    date_today=int(time.strftime("%Y%m%d"))
    for product in results:
        update_date=int(str(product.pub_date).split(' ')[0].replace('-',''))
        if date_today-update_date>=2:
            continue
        item={}
        product_price=float(product.price)
        for price in prices:
            price_from=price.price_from
            price_to=price.price_to
            price_add=price.price_add
            if product_price>=price_from and product_price<price_to:
                product_price+=price_add
                break
        item['price']=product_price
        item['goodsName']=product.goodsName
        item['brand']=product.brand
        item['goodsNum']=product.goodsNum
        items.append(item)
    return render(request,'items.html',{'brand':brand,'items':items,'phone_brands':phone_brands,'tablet_brands':tablet_brands})

def item(request):
    phone_brands=[]
    tablet_brands=[]
    allow_phones=get_allow_phone_brands()
    allow_tablets=get_allow_tablet_brands()
    for item in get_phone_brands():
        if item in allow_phones:
            phone_brands.append(item)
    for item in get_tablet_brands():
        if item in allow_tablets:
            tablet_brands.append(item)
    try:
        goodsNum=request.GET['goodsNum']
    except:
        return index(request)
    item=get_item(goodsNum)
    if item==False:
        return index(request)
    products=[]
    prices=get_priceadd()
    for product in eval(item.products):
        try:
            product_price=product['price'].replace('￥','')
            product_price=float(product_price)
        except:
            products.append(product.infor+[product['price']])
            continue
        for price in prices:
            price_from=price.price_from
            price_to=price.price_to
            price_add=price.price_add
            if product_price>=price_from and product_price<price_to:
                product_price+=price_add
                break
        products.append(product['infor']+['￥'+str(product_price)])
    configuration=eval(item.configuration)
    des=eval(item.des)
    return render(request,'item.html',{'title':item.goodsName,'des':des,'configuration':configuration,'products':products,'phone_brands':phone_brands,'tablet_brands':tablet_brands})

def about(request):
    phone_brands=[]
    tablet_brands=[]
    allow_phones=get_allow_phone_brands()
    allow_tablets=get_allow_tablet_brands()
    for item in get_phone_brands():
        if item in allow_phones:
            phone_brands.append(item)
    for item in get_tablet_brands():
        if item in allow_tablets:
            tablet_brands.append(item)
    abouts=[]
    for item in get_about():
        abouts.append(item.infor)
    return render(request,'about.html',{'abouts':abouts,'phone_brands':phone_brands,'tablet_brands':tablet_brands})

def search(request):
    phone_brands=[]
    tablet_brands=[]
    allow_phones=get_allow_phone_brands()
    allow_tablets=get_allow_tablet_brands()
    for item in get_phone_brands():
        if item in allow_phones:
            phone_brands.append(item)
    for item in get_tablet_brands():
        if item in allow_tablets:
            tablet_brands.append(item)
    try:
        keyword=request.GET['keyword']
        keyword=keyword.replace(' ','').replace('-','').lower()
    except:
        pass
    results=sql_search(keyword)
    items=[]
    prices=get_priceadd()
    for product in results:
        item={}
        product_price=float(product.price)
        for price in prices:
            price_from=price.price_from
            price_to=price.price_to
            price_add=price.price_add
            if product_price>=price_from and product_price<price_to:
                product_price+=price_add
                break
        item['price']=product_price
        item['goodsName']=product.goodsName
        item['brand']=product.brand
        item['goodsNum']=product.goodsNum
        items.append(item)
    return render(request,'items.html',{'items':items,'phone_brands':phone_brands,'tablet_brands':tablet_brands})
