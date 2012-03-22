from django.conf.urls.defaults import *
from satchmo_store.urls import urlpatterns
from satchmo_utils.urlhelper import replace_urlpattern
from product.urls import catpatterns


replacement = url(r'^(?P<parent_slugs>([-\w]+/)*)?(?P<slug>[-\w]+)/$','store.category_view_kamel', {}, name='satchmo_category')

replace_urlpattern(catpatterns, replacement)
urlpatterns += patterns('',
    (r'', include('store.localsite.urls')))