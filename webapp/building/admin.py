from django import forms
from django.contrib import admin
from postgres.fields import JSONField

from .models import Building


class BuildingModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Building, BuildingModelAdmin)
