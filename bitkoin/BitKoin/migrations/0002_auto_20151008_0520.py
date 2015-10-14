# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BitKoin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receiving',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rec', models.CharField(max_length=26)),
                ('t_time_rec', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Sending',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('send', models.CharField(max_length=26)),
                ('t_time_send', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('trans_id', models.AutoField(serialize=False, primary_key=True)),
                ('trans_type', models.TextField()),
                ('t_time', models.DateTimeField()),
                ('u_trans', models.ForeignKey(to='BitKoin.UserPr')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('wallet_id', models.AutoField(serialize=False, primary_key=True)),
                ('balance', models.DecimalField(max_digits=19, decimal_places=10)),
                ('user_wallet', models.ForeignKey(to='BitKoin.UserPr')),
            ],
        ),
        migrations.AddField(
            model_name='sending',
            name='trans_id_send',
            field=models.ForeignKey(to='BitKoin.Transactions'),
        ),
        migrations.AddField(
            model_name='sending',
            name='wallet_id_send',
            field=models.ForeignKey(to='BitKoin.Wallet'),
        ),
        migrations.AddField(
            model_name='receiving',
            name='trans_id_rec',
            field=models.ForeignKey(to='BitKoin.Transactions'),
        ),
        migrations.AddField(
            model_name='receiving',
            name='wallet_id_rec',
            field=models.ForeignKey(to='BitKoin.Wallet'),
        ),
    ]
