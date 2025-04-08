from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from addresses.models import Address  # Import Address model
from .forms import UserCreationForm

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ('street', 'city', 'state', 'postal_code', 'country', 'is_default')
    verbose_name = 'آدرس'
    verbose_name_plural = 'آدرس‌ها'

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('username', 'user_type', 'is_staff', 'is_active', 'get_address_count')
    list_filter = ('user_type', 'is_staff', 'is_active')
    inlines = [AddressInline]  # Add addresses inline
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('email', 'first_name', 'last_name', 'birth_date')}),  # Removed address from here
        ('دسترسی‌ها', {'fields': ('user_type', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌های مهم', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'user_type', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    def get_address_count(self, obj):
        return obj.addresses.count()  # Using the related_name from Address model
    get_address_count.short_description = 'تعداد آدرس‌ها'

admin.site.register(User, UserAdmin)