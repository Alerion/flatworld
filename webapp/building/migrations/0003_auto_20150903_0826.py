# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0002_building_unique'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='unique',
        ),
        migrations.AlterField(
            model_name='building',
            name='build_time',
            field=models.IntegerField(help_text='in seconds for default speed'),
        ),
    ]
