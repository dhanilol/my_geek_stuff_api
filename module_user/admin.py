import binascii
import os

from django.contrib import admin

from module_user.models import ApiKey


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'updated')

    fieldsets = (
        ('Required Information', {
            'fields': ('name', )
        }),
    )

    search_fields = ('id', 'name')

    def has_delete_permission(self, request, obj=None):
        return False

    # TODO: figure out why this isn't working!!! -priority
    def save_model(self, request, obj, form, change):
        if not obj.key:
            key = binascii.hexlify(os.urandom(32)).decode()
            while ApiKey.objects.find(key=key).count() > 0:
                key = binascii.hexlify(os.urandom(32)).decode()
            obj.key = key
        obj.save()


admin.site.register(ApiKey, ApiKeyAdmin)
