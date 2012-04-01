from django import template
from product.models import Product
register = template.Library()

@register.inclusion_tag('new_arrivals.html')
def show_new_arrivals(number):
    new_arrivals = Product.objects.all().order_by('date_added')[:number]
    return {'new_arrivals': new_arrivals}

@register.inclusion_tag('featured_items.html')
def show_featured_items(number):
    featured_items = Product.objects.filter(featured=True)[:number]
    return {'featured_items': featured_items}