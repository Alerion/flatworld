from django.contrib import admin

from .models import World, Region, City


class WorldModelAdmin(admin.ModelAdmin):
    pass


class RegionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'world')
    list_filter = ('world',)


class CityModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'world', 'region', 'capital', 'user')
    list_filter = ('world',)

admin.site.register(World, WorldModelAdmin)
admin.site.register(Region, RegionModelAdmin)
admin.site.register(City, CityModelAdmin)
