"""
优惠券管理后台

支持:
  - 优惠券模板 CRUD
  - 管理员批量发放优惠券给用户
  - 查看用户优惠券和积分流水
"""

from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from django import forms
from .models import Coupon, UserCoupon, PointsTransaction


# ==================== 发放表单 ====================

class DistributeForm(forms.Form):
    """管理员发放优惠券表单"""
    user_ids = forms.CharField(
        label='用户ID列表',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': '每行一个用户ID，或用逗号分隔'}),
        help_text='输入用户ID，每行一个或用逗号分隔'
    )
    count = forms.IntegerField(
        label='每人发放数量',
        min_value=1,
        max_value=100,
        initial=1,
        help_text='每个用户发放几张优惠券'
    )


# ==================== Coupon 管理 ====================

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'discount_type', 'discount_value', 'min_amount',
                    'valid_from', 'valid_to', 'remaining', 'is_active']
    list_filter = ['discount_type', 'is_active']
    search_fields = ['code', 'name']
    fieldsets = [
        ('基本信息', {'fields': ['code', 'name', 'description']}),
        ('优惠规则', {'fields': ['discount_type', 'discount_value', 'min_amount']}),
        ('有效期', {'fields': ['valid_from', 'valid_to']}),
        ('库存', {'fields': ['total_count', 'is_active']}),
    ]

    def remaining(self, obj):
        return obj.remaining
    remaining.short_description = '剩余数量'

    actions = ['distribute_coupons']

    def distribute_coupons(self, request, queryset):
        """管理员操作：发放选中优惠券给用户"""
        if queryset.count() != 1:
            self.message_user(request, '请只选择一张优惠券进行发放', level=messages.WARNING)
            return

        coupon = queryset.first()

        if request.POST.get('confirm'):
            form = DistributeForm(request.POST)
            if form.is_valid():
                # 解析用户ID
                raw = form.cleaned_data['user_ids']
                user_ids = []
                for line in raw.replace('，', ',').split('\n'):
                    for part in line.split(','):
                        part = part.strip()
                        if part and part.isdigit():
                            user_ids.append(int(part))

                count = form.cleaned_data['count']
                from apps.users.models import User

                # 过滤存在的用户
                exist_users = User.objects.filter(id__in=user_ids).values_list('id', flat=True)
                exist_set = set(exist_users)
                not_found = set(user_ids) - exist_set

                # 批量发放
                created = 0
                batch = []
                for uid in exist_set:
                    for _ in range(count):
                        batch.append(UserCoupon(user_id=uid, coupon=coupon))
                    if len(batch) >= 100:
                        UserCoupon.objects.bulk_create(batch)
                        created += len(batch)
                        batch = []

                if batch:
                    UserCoupon.objects.bulk_create(batch)
                    created += len(batch)

                coupon.used_count += created
                coupon.save(update_fields=['used_count'])

                msg = f'成功发放 {created} 张优惠券'
                if not_found:
                    msg += f'；未找到用户ID: {not_found}'
                self.message_user(request, msg, level=messages.SUCCESS)
                return redirect('..')
        else:
            form = DistributeForm(initial={'count': 1})

        return render(request, 'admin/coupon_distribute.html', {
            'form': form,
            'coupon': coupon,
            'title': f'发放优惠券: {coupon.name}',
        })

    distribute_coupons.short_description = '发放选中优惠券给用户'
    distribute_coupons.allowed_permissions = ['change']


# ==================== UserCoupon 管理 ====================

@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ['user', 'coupon', 'status', 'received_at', 'used_at']
    list_filter = ['status']
    search_fields = ['user__username', 'coupon__code']
    actions = ['mark_expired']

    def mark_expired(self, request, queryset):
        updated = queryset.filter(status='unused').update(status='expired')
        self.message_user(request, f'已将 {updated} 张优惠券标记为已过期')
    mark_expired.short_description = '标记选中优惠券为已过期'


# ==================== PointsTransaction 管理 ====================

@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'balance', 'type', 'description', 'created_at']
    list_filter = ['type']
    search_fields = ['user__username', 'description']
    readonly_fields = ['user', 'amount', 'balance', 'type', 'description', 'order', 'created_at']
