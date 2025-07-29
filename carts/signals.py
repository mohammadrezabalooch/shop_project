from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.db.models import F
from .models import Cart, CartItem
from django.core.exceptions import ValidationError


@receiver(pre_save, sender=CartItem)
def update_stock_on_cart_item_save(sender, instance, **kwarg):
    product = instance.item

    if instance.pk:
        old_item = CartItem.objects.get(pk=instance.pk)
        quantity_diff = instance.quantity - old_item.quantity
    else:
        quantity_diff = instance.quantity

    if product.stock < quantity_diff:
        raise ValidationError(
            f"موجودی محصول {product.name} برای افزودن {quantity_diff} عدد کافی نیست."
        )

    product.stock = F("stock") - quantity_diff
    product.save(update_fields=["stock"])


# @receiver(pre_delete, sender=Cart)
# def return_stock_on_cart_delete(sender, instance, **kwargs):
#     for cart_item in instance.items.all():
#         product = cart_item.item
#         product.stock = F("stock") + cart_item.quantity
#         product.save(update_fields=["stock"])
#     print(
#         f"موجودی محصولات مربوط به سبد خرید کاربر {instance.user.username} بازگردانده شد."
#     )

# سیگنالی که برای pre_delete مدل cartitem نوشتم موقع delete مدل cart اجرا میشه
# اگر سیگنال بالا رو نگه دارم موقع حذف سبد خرید دوبرابر تعداد ایتمای لیست به موجودی کالا اضافه میشه که اشتباهه
# درواقع موقع دلیت کارت دونه دونه همه کارت ایتما دلیت میشن و با اجرا دلیت سیگنال pre_delete هم کار میکنه


@receiver(pre_delete, sender=CartItem)
def return_stock_on_cart_item_delete(sender, instance, **kwargs):
    product = instance.item
    product.stock = F("stock") + instance.quantity
    product.save(update_fields=["stock"])
