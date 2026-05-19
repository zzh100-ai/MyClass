from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['course', 'course_title', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'user', 'total_amount', 'final_amount', 'coupon_discount',
                    'points_discount', 'status', 'created_at', 'paid_at']
    list_filter = ['status']
    search_fields = ['order_no', 'user__username']
    inlines = [OrderItemInline]
