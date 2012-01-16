# -*- coding: utf-8 -*-
import sys
import xlrd
import copy
import tax.config
from decimal import Decimal
from os.path import join, abspath, dirname
# adjust path if needed, assumes this file is located in a folder
# inside your project
sys.path.append(dirname(dirname(abspath(__file__))))
from django.core.management import setup_environ
from django.contrib.sites.models import Site
from product.models import *
from product.modules.configurable.models import ConfigurableProduct, ProductVariation

"""
Modify the row indexes according to your excel file.
The file I used looks like this (not all rows used in importer):

product id;child id(for variations);extra code;product name;category;-;-;-;price;-;short desc;long desc;in stock;-;color;weight;weight unit;length;length unit;width;width unit;height;height unit;image path
"""

def import_products():
    """
    Import excel data into satchmo.
    """
    book = xlrd.open_workbook(
        join(dirname(abspath(__file__)), 'kwiaty.xls'))
    sheet = book.sheet_by_index(0)
    # create the categories first
#    categories = []
#    for row_no in range(1, sheet.nrows):
#        row = sheet.row_values(row_no)
#        # mulitple categories can by separated with pipe
#        for category in row[4].split('|'):
#            if not category in categories:
#                categories.append(category)
    #for category in categories:
       # _create_category(category)
    # if needed, create product attribute(s) here
    #_create_product_attribute()

    # continue with products
    for row_no in range(1, sheet.nrows):
        row = sheet.row_values(row_no)
        _create_product(row)
        # if needed, create product variation
        #_create_product_variation(row):
    # refresh lookup
    ProductPriceLookup.objects.rebuild_all()

def _create_category(name, parent=None):
    """
    Create a category. Calls itself when hierarchy is needed.
    """
    cat = _find_category(name)
    print cat
#    if '/' in name:
#        # parent/child categories can be created with /
#        parent = None
#        for hier_category in name.split('/'):
#            parent = _create_category(hier_category, parent)
#        return
#    try:
#        print name
#        cat = _find_category(name)
#        #cat = Category.objects.get(name=name)
#    except Category.DoesNotExist:
#        cat = Category(name=name)
#        if parent is not None:
#            cat.parent = parent
#        cat.site = Site.objects.get(id=1)
#        cat.save()
#    else:
#        if parent is not None:
#            cat = Category(name=name)
#            cat.parent = parent
#            cat.site = Site.objects.get(id=1)
#            cat.save()
    return cat

def _find_category(name):
    parent = None
    for sub_name in name.split('/'):
        if parent is not None:
            category = Category.objects.get(name=sub_name, parent=parent)
        else:
            category = Category.objects.get(name=sub_name)
        parent = category
    return category

def _create_product_attribute():
    try:
        AttributeOption.objects.get(name='extra')
    except AttributeOption.DoesNotExist:
        option = AttributeOption(description='Something')
        option.name = 'extra'
        option.validation = 'product.utils.validation_simple'
        option.sort_order = 99
        option.error_message = 'extra missing'
        option.save()
    else:
        pass

def _add_product_attribute(product, attr_name, value):
    pattr = ProductAttribute(product=product)
    pattr.languagecode = 'en'
    pattr.option = AttributeOption.objects.get(name=attr_name)
    pattr.value = value
    pattr.save()

def _create_product(row):
    p = Product(name=row[3])
    p.site = Site.objects.get(id=1)
    p.sku = '%s' % row[5]
    p.short_description = row[10]
    p.description = row[11]
    p.save()
    # find the category to add
    for category_name in row[4].split(','):
        category = _find_category(category_name)
        p.category.add(category)
    if row[12]:
        p.items_in_stock = Decimal(str(row[12]))
    try:
        float(row[15])
    except:
        pass
    else:
        p.weight = Decimal(str(row[15]))
    p.weight_units = row[16]
    if row[17]:
        p.length = Decimal(str(row[17]))
    p.length_units = row[18]
    if row[19]:
        p.width = Decimal(str(row[19]))
    p.width_units = row[20]
    if row[21]:
        p.height = Decimal(str(row[21]))
    p.height_units = row[22]
    p.taxClass = TaxClass.objects.get(title='Kartka')
    p.taxable = True
    p.save()
    # add a product attribute
    if row[2]:
        _add_product_attribute(p, 'extra', row[2])
    # add price
    price = Price(product=p)
    price.price = Decimal(str(row[8]))
    price.save()
    # add image
    if row[23]:
        image = ProductImage(product=p)
        image.picture = row[23].replace('\\', '/')
        image.save()

def _create_product_variation(row):
    """
    Manually create all objects for a new product option.
    This includes (if not existing):
        Option
        OptionGroup
        Product
        ConfigurableProduct
        ProductVariation

    You could also use the create_subs flag from ConfigurableProduct which
    creates the variations automatically for you, but you're then loosing the
    ability to manually set the SKU etc.
    """
    # get option group or create if not existing
    try:
        group = OptionGroup.objects.get(name=row[4])
    except OptionGroup.DoesNotExist:
        group = OptionGroup(site=Site.objects.get(id=1))
        group.name = row[4]
        group.description = ''
        group.save()
    # create the new option
    option = Option(option_group=group)
    option.name = row[3]
    option.value = row[3]
    option.sort_order = int(row[1])
    option.save()
    # now first create a Product...
    product = _create_product(row)
    # variants dont need a category, otherwise they show up as normal products
    product.category.clear()
    # then get or create the ConfigurableProduct and add the option group
    # somehow the root product to which all variations belong must be
    # identified, in this case the variation id is 00
    main_product = Product.objects.get(sku='%s' % row[5])
    try:
        cp = ConfigurableProduct.objects.get(product=main_product)
    except ConfigurableProduct.DoesNotExist:
        cp = ConfigurableProduct(product=main_product)
        cp.save()
        cp.option_group.add(group)
        cp.save()
    # finally create the ProductVariation and add the option
    variation = ProductVariation(product=product)
    variation.parent = cp
    variation.save()
    variation.options.add(option)
    variation.save()

if __name__ == '__main__':
    #Option.objects.all().delete()
    #Product.objects.all().delete()
    #AttributeOption.objects.all().delete()
    #ProductAttribute.objects.all().delete()
    import_products()