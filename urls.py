from django.conf.urls.defaults import *
from satchmo_utils.urlhelper import replace_urlpattern
from product.urls.category import urlpatterns

replacement=patterns('product.views',
    (r'^(?P<parent_slugs>([-\w]+/)*)?(?P<slug>[-\w]+)/$',
        'category_view_kamel', {}, 'satchmo_category'),
    (r'^$', 'category_index', {}, 'satchmo_category_index'),
)
replace_urlpattern(urlpatterns,replacement)

