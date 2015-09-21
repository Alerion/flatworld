from django.contrib import admin

from .models import Type, Unit


class UnitModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'parent', 'attack', 'defence')


admin.site.register(Type)
admin.site.register(Unit, UnitModelAdmin)
