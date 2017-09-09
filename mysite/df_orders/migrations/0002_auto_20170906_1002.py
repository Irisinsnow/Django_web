# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbasic',
            name='order_id',
            field=models.CharField(max_length=64, serialize=False, primary_key=True, verbose_name='订单id'),
        ),
        migrations.AlterField(
            model_name='orderbasic',
            name='transit_price',
            field=models.DecimalField(max_digits=10, verbose_name='订单运费', decimal_places=2),
        ),
    ]
