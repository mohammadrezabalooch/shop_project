from django import template
from carts.models import Cart, CartItem
from products.models import Product

register = template.Library()


@register.simple_tag
def get_cart_item(cart, product):
    return cart.items.filter(item=product).first()
