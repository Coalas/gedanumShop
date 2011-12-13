from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from livesettings import config_value
from product.views import display_featured
from satchmo_utils.views import bad_or_missing

def category_view_kamel(request, slug, parent_slugs='', template='product/category.html'):
    """Display the category, its child categories, and its products.

    Parameters:
     - slug: slug of category
     - parent_slugs: ignored
    """
    if request.method == "GET":
        currpage = request.GET.get('page', 1)
    else:
        currpage = 1
        
    is_paged = False
    page = None
        
    try:
        category =  Category.objects.get_by_site(slug=slug)
        products = list(category.active_products())
        sale = find_best_auto_discount(products)
        count = config_value('PRODUCT','NUM_PAGINATED')
        paginator = Paginator(products, count)
        try:
            paginator.validate_number(currpage)
        except EmptyPage:
            return bad_or_missing(request, _("Invalid page number"))
        is_paged = paginator.num_pages > 1
        page = paginator.page(currpage)
    
    except Category.DoesNotExist:
        return bad_or_missing(request, _('The category you have requested does not exist.'))

    child_categories = category.get_all_children()

    ctx = {
        'category': category,
        'child_categories': child_categories,
        'sale' : sale,
        'products' : page.object_list,
        'is_paginated' : is_paged,
        'page_obj' : page,
        'paginator' : paginator
    }
    index_prerender.send(Product, request=request, context=ctx, category=category, object_list=products)
    return render_to_response(template, context_instance=RequestContext(request, ctx))