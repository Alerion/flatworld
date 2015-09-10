from django.contrib import admin

from .models import Building


class BuildingModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'build_time', 'cost_money', 'cost_population', 'properties')

admin.site.register(Building, BuildingModelAdmin)
