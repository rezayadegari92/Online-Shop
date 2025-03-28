from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'user_type'),
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'is_staff', 'is_active'),
        }),
    )
    
    def get_fieldsets(self, request, obj=None):
        """Show name fields as required only for customers"""
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.is_customer:
            # Modify fieldsets to mark names as required for customers
            fieldsets = list(fieldsets)
            personal_info = list(fieldsets[1][1]['fields'])
            if 'first_name' in personal_info and 'last_name' in personal_info:
                fieldsets[1][1]['description'] = 'Required fields for customers'
        return fieldsets
    
    def save_model(self, request, obj, form, change):
        """Ensure validation is run on admin save"""
        obj.full_clean()
        super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)