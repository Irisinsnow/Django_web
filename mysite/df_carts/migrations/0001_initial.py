# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('goods_count', models.IntegerField(default=1, verbose_name='商品数目')),
            ],
            options={
                'db_table': 's_cart',
            },
        ),
    ]
