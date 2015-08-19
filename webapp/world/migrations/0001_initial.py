# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Biome',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('border', models.BooleanField()),
                ('coast', models.BooleanField()),
                ('ocean', models.BooleanField()),
                ('water', models.BooleanField()),
                ('river', models.BooleanField()),
                ('biome', models.CharField(max_length=50, choices=[('BARE', 'Bare'), ('BEACH', 'Beach'), ('GRASSLAND', 'Grassland'), ('ICE', 'Ice'), ('LAKE', 'Lake'), ('MARSH', 'Marsh'), ('OCEAN', 'OCEAN'), ('SCORCHED', 'Scorched'), ('SHRUBLAND', 'Shrubland'), ('SNOW', 'Snow'), ('SUBTROPICAL_DESERT', 'Subtropical deset'), ('TAIGA', 'Taiga'), ('TEMPERATE_DECIDUOUS_FOREST', 'Deciduous foreset'), ('TEMPERATE_DESERT', 'Desert'), ('TEMPERATE_RAIN_FOREST', 'Rain forest'), ('TROPICAL_RAIN_FOREST', 'Tropical rain forest'), ('TROPICAL_SEASONAL_FOREST', 'Tropical seasonal forest'), ('TUNDRA', 'Tundra')])),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('elevation', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('moisture', models.FloatField()),
                ('neighbors', models.ManyToManyField(to='world.Biome', related_name='neighbors_rel_+')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('capital', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('coords', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('biome', models.ForeignKey(to='world.Biome')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('name', models.CharField(max_length=100)),
                ('neighbors', models.ManyToManyField(to='world.Region', related_name='neighbors_rel_+')),
            ],
        ),
        migrations.CreateModel(
            name='River',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
                ('width', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='World',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('seed', models.DecimalField(max_digits=20, decimal_places=0)),
                ('points', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='river',
            name='world',
            field=models.ForeignKey(to='world.World'),
        ),
        migrations.AddField(
            model_name='region',
            name='world',
            field=models.ForeignKey(to='world.World'),
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(to='world.Region'),
        ),
        migrations.AddField(
            model_name='city',
            name='world',
            field=models.ForeignKey(to='world.World'),
        ),
        migrations.AddField(
            model_name='biome',
            name='region',
            field=models.ForeignKey(to='world.Region', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='biome',
            name='world',
            field=models.ForeignKey(to='world.World'),
        ),
    ]
