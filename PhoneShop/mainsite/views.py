from .inquery import *
from django.shortcuts import render
from django.http import HttpResponse
from django.http  import HttpResponseRedirect
from django.template.loader import render_to_string
# Create your views here.

def index(request):
    phone_brands=get_phone_brands()
    tablet_brands=get_tablet_brands()
    return render(request,'index.html',{'phone_brands':phone_brands,'tablet_brands':tablet_brands})

def smartphone(request):
    phone_brands=get_phone_brands()
    tablet_brands=get_tablet_brands()
    try:
        brand=request.GET['brand']
    except:
        brand=''
    results=get_phones(brand)
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
    return render(request,'items.html',{'brand':brand,'items':items,'phone_brands':phone_brands,'tablet_brands':tablet_brands})

def tablets(request):
    phone_brands=get_phone_brands()
    tablet_brands=get_tablet_brands()
    try:
        brand=request.GET['brand']
    except:
        brand=''
    results=get_tablets(brand)
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
    return render(request,'items.html',{'brand':brand,'items':items,'phone_brands':phone_brands,'tablet_brands':tablet_brands})

def item(request):
    phone_brands=get_phone_brands()
    tablet_brands=get_tablet_brands()
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

def contact(request):
    phone_brands=get_phone_brands()
    tablet_brands=get_tablet_brands()
    return render(request,'contact.html',{'phone_brands':phone_brands,'tablet_brands':tablet_brands})

def about(request):
    phone_brands=get_phone_brands()
    tablet_brands=get_tablet_brands()
    return render(request,'about.html',{'phone_brands':phone_brands,'tablet_brands':tablet_brands})
