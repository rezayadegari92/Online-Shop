# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Account

class AccountCreationForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=Account.Role.choices,
        initial=Account.Role.CUSTOMER,
        help_text="Select the role for this user"
    )

    class Meta:
        model = Account
        fields = ('email', 'role')

class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser',
                      'groups', 'user_permissions'),
        }),
        ('Customer Details', {
            'fields': ('first_name', 'last_name', 'birth_date'),
            'classes': ('collapse',),
        }),
    )
    list_display = ('email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not obj or obj.role != Account.Role.CUSTOMER:
            fieldsets = [fs for fs in fieldsets if fs[0] != 'Customer Details']
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.role == Account.Role.CUSTOMER:
            form.base_fields['first_name'].required = True
            form.base_fields['last_name'].required = True
            form.base_fields['birth_date'].required = True
        return form

    class Media:
        js = ('admin/js/role_handler.js',)

admin.site.register(Account, AccountAdmin)