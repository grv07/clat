# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models
import teacher.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('user_login', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('uuid_key', models.TextField(max_length=100)),
                ('full_name', models.TextField(max_length=100)),
                ('phone_number', models.CharField(unique=True, max_length=15, validators=[teacher.validators.phone_regex])),
                ('gender', models.CharField(max_length=50, null=True)),
                ('d_o_b', models.DateField(null=True)),
                ('higher_education', models.TextField(max_length=100, null=True)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('i_agree', models.BooleanField(default=False)),
                ('address', models.OneToOneField(to='user_login.Address')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
