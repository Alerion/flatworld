# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0005_auto_20150910_0812'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Building',
        ),
    ]
