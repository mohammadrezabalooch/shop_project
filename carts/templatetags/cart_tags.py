from django import template

register = template.Library()


@register.simple_tag
def get_cart_item(cart, product):
    if cart and hasattr(cart, "items"):
        return cart.items.filter(item=product).first()
    return None
