from django.db import models

# Create your models here.
class Phone(models.Model):
    goodsNum=models.CharField(u"ID",max_length=20,primary_key=True)
    price=models.CharField(u"Price",max_length=30)
    goodsName=models.CharField(u"Name",max_length=80)
    brand=models.CharField(u"品牌",max_length=80)
    pub_date = models.CharField(u'更新时间',max_length=80)
    products=models.TextField(u"产品")
    des=models.TextField("详情")
    configuration=models.TextField("配置")

class Tablet(models.Model):
     goodsNum=models.CharField(u"ID",max_length=20,primary_key=True)
     price=models.CharField(u"Price",max_length=30)
     goodsName=models.CharField(u"Name",max_length=80)
     brand=models.CharField(u"品牌",max_length=80)
     pub_date = models.CharField(u'更新时间',max_length=80)
     products=models.TextField(u"产品")
     des=models.TextField("详情")
     configuration=models.TextField("配置")

class Price(models.Model):
    price_from=models.IntegerField("PriceFrom")
    price_to=models.IntegerField("PriceTo")
    price_add=models.IntegerField("加价")

class About(models.Model):
    infor=models.TextField(u"内容")
    pub_date = models.DateTimeField(u'更新时间', auto_now_add=True, editable = True)

class Announcement(models.Model):
    infor=models.TextField(u"内容")
    pub_date = models.DateTimeField(u'更新时间', auto_now_add=True, editable = True)

class AllowPhoneBrand(models.Model):
    brand=models.CharField(u"品牌",max_length=80)
    pub_date = models.DateTimeField(u'更新时间', auto_now_add=True, editable = True)

class AllowTabletBrand(models.Model):
    brand=models.CharField(u"品牌",max_length=80)
    pub_date = models.DateTimeField(u'更新时间', auto_now_add=True, editable = True)
