# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150924_0847'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quest',
            old_name='city',
            new_name='cities',
        ),
        migrations.RenameField(
            model_name='quest',
            old_name='region',
            new_name='regions',
        ),
    ]
