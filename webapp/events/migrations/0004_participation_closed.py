# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150924_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='closed',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
