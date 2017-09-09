# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
        ('df_carts', '0001_initial'),
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='goods',
            field=models.ForeignKey(to='df_goods.Goods', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='cart',
            name='passport',
            field=models.ForeignKey(to='df_user.Passport', verbose_name='账户'),
        ),
    ]
