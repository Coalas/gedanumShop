#
#   DOTPAY / ServiRed payments module for Satchmo
#
#   Author: Michal Salaban <michal (at) salaban.info>
#   with a great help of Fluendo S.A., Barcelona
#
#   Based on "Guia de comercios TPV Virtual SIS" ver. 5.18, 15/11/2008, DOTPAY
#   For more information about integration look at http://www.dotpay.es/
#
#   TODO: DOTPAY interface provides possibility of recurring payments, which
#   could be probably used for SubscriptionProducts. This module doesn't support it.
#
from django.conf.urls.defaults import patterns
from satchmo_store.shop.satchmo_settings import get_satchmo_setting

ssl = get_satchmo_setting('SSL', default_value=False)

urlpatterns = patterns('',
    (r'^$', 'payment.modules.dotpay.views.pay_ship_info', {'SSL': ssl}, 'DOTPAY_satchmo_checkout-step2'),
    (r'^confirm/$', 'payment.modules.dotpay.views.confirm_info', {'SSL': ssl}, 'DOTPAY_satchmo_checkout-step3'),
    (r'^success/$', 'payment.modules.dotpay.views.success', {'SSL': ssl}, 'DOTPAY_satchmo_checkout-success'),
    (r'^failure/$', 'payment.views.checkout.failure', {'SSL': ssl}, 'DOTPAY_satchmo_checkout-failure'),
    (r'^notify/$', 'payment.modules.dotpay.views.notify_callback', {'SSL': ssl}, 'DOTPAY_satchmo_checkout-notify_callback'),
    (r'^confirmorder/$','payment.views.confirm.confirm_free_order', {'SSL' : ssl, 'key' : 'DOTPAY'}, 'DOTPAY_satchmo_checkout_free-confirm')
)
