# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assesment_engine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assesmentregisterduser',
            name='remaning_attempts',
            field=models.IntegerField(default=b'0'),
        ),
    ]
