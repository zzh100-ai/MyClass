from celery import shared_task
from django.utils.timezone import now


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def cancel_expired_order(self, order_id):
    """
    取消超时未支付的订单

    触发方式：下单时通过 apply_async(countdown=30min) 调度
    取消逻辑：
    1. 检查订单是否仍为 pending
    2. 将状态改为 cancelled
    3. 如有关联优惠券，恢复为未使用
    """
    from .models import Order

    try:
        order = Order.objects.select_related('user_coupon').get(id=order_id)
    except Order.DoesNotExist:
        return {'status': 'not_found', 'order_id': order_id}

    # 只有待支付的订单才取消
    if order.status != Order.Status.PENDING:
        return {'status': 'skipped', 'order_id': order_id, 'reason': f'订单状态为{order.status}'}

    order.status = Order.Status.CANCELLED
    order.save(update_fields=['status'])

    # 恢复优惠券为未使用
    if order.user_coupon and order.user_coupon.status == 'used':
        order.user_coupon.status = 'unused'
        order.user_coupon.save(update_fields=['status'])

    return {'status': 'cancelled', 'order_id': order_id}
