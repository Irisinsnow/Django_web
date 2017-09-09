# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('recipient_name', models.CharField(verbose_name='收件人', max_length=20)),
                ('recipient_addr', models.CharField(verbose_name='收件人地址', max_length=256)),
                ('recipient_phone', models.CharField(verbose_name='收件人的电话', max_length=11)),
                ('zip_code', models.CharField(verbose_name='邮政编码', max_length=6)),
                ('is_def', models.BooleanField(default=False, verbose_name='是否默认')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('username', models.CharField(verbose_name='用户名', max_length=20)),
                ('password', models.CharField(verbose_name='密码', max_length=40)),
                ('email', models.EmailField(verbose_name='用户邮箱', max_length=254)),
            ],
            options={
                'db_table': 's_user_account',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='passport',
            field=models.ForeignKey(verbose_name='所属账户', to='df_user.Passport'),
        ),
    ]
