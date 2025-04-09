# addresses/admin.py
from django.contrib import admin
from .models import Address
from django.utils.html import format_html

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'street', 'city', 'state', 'postal_code', 'country', 'phone_number','is_default')
    list_filter = ('country', 'state', 'is_default')
    search_fields = ('city', 'street', 'user__username', 'user__email')
    raw_id_fields = ('user',)  # Useful for large user databases
    list_editable = ('is_default',)
    ordering = ('-is_default', 'city')

    def user_info(self, obj):
        return format_html(
            '{}<br><small>{}</small>',
            obj.user.username,
            obj.user.email
        )
    user_info.short_description = 'User'

    def is_default_display(self, obj):
        return '✅' if obj.is_default else '❌'
    is_default_display.short_description = 'Default'

    fieldsets = (
        ('User Relation', {
            'fields': ('user', 'is_default')
        }),
        ('Address Details', {
            'fields': (
                ('street', 'city'),
                ('state', 'postal_code', 'phone_number'),
                'country'
            )
        }),
    )