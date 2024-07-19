from django import template

register = template.Library()

@register.simple_tag()
def multiply(x,y):
    return x*y

@register.simple_tag()
def find_item_amount(item, objects):
    for object in objects:
        if object.item == item:
            return object.amount
    return 0

@register.simple_tag()
def total_price(purchases):
    sum = 0
    for purchase in purchases:
        sum += purchase.item.price * purchase.amount
    return sum