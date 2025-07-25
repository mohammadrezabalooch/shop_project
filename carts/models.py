from django.db import models

# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(
        "accounts.CustomUser", on_delete=models.CASCADE, related_name="cart"
    )

    def __str__(self):
        return f"سبد خرید {self.user.username}"

    def cart_total_price(self):
        total = 0
        for item in self.items.all():
            # total += item.quantity * item.item.price
            total += item.item_total_price()
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def item_total_price(self):
        return self.item.price * self.quantity
