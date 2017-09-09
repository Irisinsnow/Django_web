# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrowseHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'db_table': 's_browse_history',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('goods_type_id', models.SmallIntegerField(choices=[(1, '新鲜水果'), (2, '海鲜水产'), (3, '朱牛羊肉'), (5, '新鲜蔬菜'), (6, '速冻食品')], verbose_name='商品种类id')),
                ('goods_name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('goods_sub_title', models.CharField(max_length=256, verbose_name='副标题')),
                ('goods_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')),
                ('transit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='运费')),
                ('goods_unite', models.CharField(max_length=20, verbose_name='单位')),
                ('goods_info', tinymce.models.HTMLField(verbose_name='商品详情')),
                ('goods_sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('goods_status', models.SmallIntegerField(default=0, verbose_name='状态')),
            ],
            options={
                'db_table': 's_goods',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('img_url', models.ImageField(upload_to='goods', verbose_name='商品图片')),
                ('is_def', models.BooleanField(default=False, verbose_name='是否默认')),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='所属商品')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
        migrations.AddField(
            model_name='browsehistory',
            name='goods',
            field=models.ForeignKey(to='df_goods.Goods', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='browsehistory',
            name='passport',
            field=models.ForeignKey(to='df_user.Passport', verbose_name='所属账户'),
        ),
    ]
