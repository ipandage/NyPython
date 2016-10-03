# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('goodsNum', models.CharField(max_length=20, verbose_name='ID')),
                ('price', models.CharField(max_length=30, verbose_name='Price')),
                ('goodsName', models.CharField(max_length=80, verbose_name='Name')),
                ('brand', models.CharField(max_length=80, verbose_name='品牌')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('products', models.TextField(verbose_name='产品')),
                ('des', models.TextField(verbose_name='详情')),
                ('configuration', models.TextField(verbose_name='配置')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('price_from', models.IntegerField(verbose_name='PriceFrom')),
                ('price_to', models.IntegerField(verbose_name='PriceTo')),
                ('price_add', models.IntegerField(verbose_name='加价')),
            ],
        ),
        migrations.CreateModel(
            name='Tablet',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('goodsNum', models.CharField(max_length=20, verbose_name='ID')),
                ('price', models.CharField(max_length=30, verbose_name='Price')),
                ('goodsName', models.CharField(max_length=80, verbose_name='Name')),
                ('brand', models.CharField(max_length=80, verbose_name='品牌')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('products', models.TextField(verbose_name='产品')),
                ('des', models.TextField(verbose_name='详情')),
                ('configuration', models.TextField(verbose_name='配置')),
            ],
        ),
    ]
