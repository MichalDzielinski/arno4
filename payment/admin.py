from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product',  'price', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(ShippingAddress)


