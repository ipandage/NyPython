from .models import Phone,Price,Tablet

def get_tablet_brands():
    brands=[]
    for item in Tablet.objects.all():
        brands.append(item.brand)
    return brands

def get_phone_brands():
    brands=[]
    for item in Phone.objects.all():
        brands.append(item.brand)
    return brands

def get_phones(brand=''):
    result=Phone.objects.filter(brand=brand)
    return result

def get_tablets(brand=''):
    result=Phone.objects.filter(brand=brand)
    return result
