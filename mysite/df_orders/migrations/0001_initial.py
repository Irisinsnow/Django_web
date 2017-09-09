# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderBasic',
            fields=[
                ('is_delete', models.BooleanField(default=False, verbose_name='删除')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('order_id', models.CharField(max_length=64, serialize=False, primary_key=True, verbose_name='订单ID')),
                ('total_count', models.IntegerField(default=1, verbose_name='商品总数')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品总额')),
                ('transit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='运费')),
                ('pay_method', models.IntegerField(default=1, verbose_name='支付方式')),
                ('order_status', models.IntegerField(default=1, verbose_name='订单状态')),
                ('addr', models.ForeignKey(to='df_user.Address', verbose_name='收件地址')),
                ('passport', models.ForeignKey(to='df_user.Passport', verbose_name='用户')),
            ],
            options={
                'db_table': 's_order_basic',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('goods_count', models.IntegerField(default=1, verbose_name='商品数目')),
                ('goods_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='商品')),
                ('order', models.ForeignKey(to='df_orders.OrderBasic', verbose_name='基本订单')),
            ],
            options={
                'db_table': 's_order_detail',
            },
        ),
    ]
