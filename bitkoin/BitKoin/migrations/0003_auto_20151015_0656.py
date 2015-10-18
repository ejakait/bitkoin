# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BitKoin', '0002_auto_20151008_0520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiving',
            name='trans_id_rec',
        ),
        migrations.RemoveField(
            model_name='receiving',
            name='wallet_id_rec',
        ),
        migrations.RemoveField(
            model_name='sending',
            name='trans_id_send',
        ),
        migrations.RemoveField(
            model_name='sending',
            name='wallet_id_send',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='u_trans',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='user_wallet',
        ),
        migrations.DeleteModel(
            name='Receiving',
        ),
        migrations.DeleteModel(
            name='Sending',
        ),
        migrations.DeleteModel(
            name='Transactions',
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
    ]
