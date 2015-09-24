from django.contrib import admin

from .models import Quest


class QuestModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'world', 'created', 'finished', 'last_till', 'repeatable', 'required')
    filter_horizontal = ('cities', 'regions')

admin.site.register(Quest, QuestModelAdmin)
