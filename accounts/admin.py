from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from addresses.models import Address  # Import Address model
from .forms import UserCreationForm



class RoleBasedAdmin(admin.ModelAdmin):
    restricted_models_for_operator = ['user', 'product']

    def is_restricted_model(self):
        model_cls = getattr(self, 'model', None)
        if not model_cls:
            return False
        if getattr(model_cls._meta, 'abstract', False):
            return False
        return model_cls._meta.model_name in self.restricted_models_for_operator

    def has_module_permission(self, request):
        if not request.user.is_authenticated:
            return False
        # اجازهٔ دیدن ماژول (اپ) در صفحهٔ اصلی ادمین
        user_type = request.user.user_type
        if user_type == 'manager':
            return True
        if user_type == 'supervisor':
            return True
        if user_type == 'operator' and not self.is_restricted_model():
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.user_type in ['manager', 'supervisor', 'operator']

    def has_add_permission(self, request):
        if not request.user.is_authenticated:
            return False
        if request.user.user_type == 'manager':
            return True
        if request.user.user_type == 'operator' and not self.is_restricted_model():
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.user_type == 'manager':
            return True
        if request.user.user_type == 'operator' and not self.is_restricted_model():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.user_type == 'manager'




class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ('street', 'city', 'state', 'postal_code', "phone_number",'country', 'is_default')
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