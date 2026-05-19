"""
动态定价引擎 — 活动-优惠类型-公式 三层抽象

定价公式:
  final_price = max(0, order_total - coupon_discount - points_discount)

TODO: 理解三层抽象
  活动层: 什么活动？（618大促 / 新用户专享 / 会员日）
  类型层: 什么优惠？（满减券 / 折扣券 / 积分抵扣）
  公式层: 怎么算？（百分比 / 固定金额 / 阶梯优惠）
"""

from decimal import Decimal
from apps.coupon.models import Coupon

POINTS_RATIO = Decimal('0.01') # 1积分 = ¥0.01

def calculate_coupon_discount(coupon, order_total):
    """
    计算优惠券优惠金额

    TODO: 理解折扣计算
    1. 百分比折扣: discount = order_total * (1 - value/100)
       → 原价200，8折券(value=80)，优惠 = 200 * 0.2 = 40
    2. 固定金额: discount = value
       → 减30券(value=30)，优惠 = 30

    注意: 优惠金额不能超过订单总额
    """
    if not coupon:
        return Decimal('0')

    if not isinstance(coupon, Coupon):
        return Decimal('0')

    if coupon.discount_type == Coupon.DiscountType.FIXED:
        discount = coupon.discount_value
    elif coupon.discount_type == Coupon.DiscountType.PERCENT:
        discount = order_total * (Decimal('1') - coupon.discount_value / Decimal('100'))
    else:
        return Decimal('0')

    return min(discount, order_total)


def calculate_final_price(order_total, user_coupon=None, points_to_use=0):
    """
    计算最终的价格
    :param order_total:
    :param coupon:
    :param points_discount:
    :return: {
              'final_price': Decimal,
              'coupon_discount': Decimal,
              'points_discount': Decimal,
              }
    """
    coupon_discount=Decimal('0')

    # 1. 优惠劵校验
    if user_coupon:
        coupon=user_coupon.coupon
        if user_coupon.status=="unused" and coupon.is_active:
            if order_total>=coupon.min_amount:
                coupon_discount=calculate_coupon_discount(coupon,order_total)

    # 积分抵扣
    points_discount=Decimal('0')
    if points_to_use>0:
        # 积分不足 -> 最多使用全部
        points_discount=min(points_to_use,order_total-coupon_discount)
        points_discount=points_discount*POINTS_RATIO

    final_price=max(Decimal('0'),order_total-coupon_discount-points_discount)

    return {
        'final_price':final_price,
        'coupon_discount':coupon_discount,
        'points_discount':points_discount,
    }
