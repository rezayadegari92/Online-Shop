from django.contrib import admin
from accounts.models import Account
from .models import Address
from django.utils.translation import gettext_lazy as _
# Register your models here.
class AddressInline(admin.TabularInline):
    model = Account.addresses.through
    extra = 1
    verbose_name = _('Address')
    verbose_name_plural = _('Addresses')



admin.site.register(Address)    