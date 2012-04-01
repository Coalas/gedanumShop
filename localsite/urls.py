from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from satchmo_store.urls import urlpatterns

#urlpatterns = patterns('',
#    (r'example/', 'store.localsite.views.example', {}),
#)
urlpatterns = patterns('',
    (r'^static_page/(?P<page>\w+)/$', 'store.localsite.views.static_page',{}),(r'^load_towns$','store.load_towns'),
)