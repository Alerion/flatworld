# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_participation_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participation',
            name='result_roll',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
