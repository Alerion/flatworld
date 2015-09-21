from django.contrib import admin

from .models import Building, BuildingTier


class BuildingTierInline(admin.StackedInline):
    model = BuildingTier
    extra = 0


class BuildingModelAdmin(admin.ModelAdmin):
    inlines = (BuildingTierInline,)
    list_display = ('name', 'max_level')

admin.site.register(Building, BuildingModelAdmin)
