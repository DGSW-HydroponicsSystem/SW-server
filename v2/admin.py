from django.contrib import admin

from .models import cropModel, currCrop


class cropModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {"fields": ('name', 'info', 'image')}),
    )
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(cropModel, cropModelAdmin)
admin.site.register(currCrop)
