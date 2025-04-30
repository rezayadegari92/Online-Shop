from django.contrib import admin
from .models import Order, OrderItem, DiscountCode
from accounts.admin import RoleBasedAdmin

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(RoleBasedAdmin):
    list_display = ("id", "user", "status", "payment_status","total_price", "shipping_address_display","created_at")
    list_filter = ("status",)
    inlines = [OrderItemInline]
    readonly_fields = ("total_price",)

    def shipping_address_display(self, obj):
        return (
            f"{obj.shipping_state}, {obj.shipping_city}, {obj.shipping_street}, "
            f"{obj.shipping_postal_code}, {obj.shipping_country} | {obj.shipping_phone_number}"
        )
    shipping_address_display.short_description = "آدرس ارسال"


@admin.register(OrderItem)
class OrderItemAdmin(RoleBasedAdmin):
    list_display = ("order", "product", "quantity", "price_at_purchase")


@admin.register(DiscountCode)
class DiscountCodeAdmin(RoleBasedAdmin):
    list_display = ("code", "discount_percent")