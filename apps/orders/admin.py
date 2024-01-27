from django.contrib import admin
from apps.orders.models import Order, Postuplenie, PublicOffer, Payment

# Register your models here.

admin.site.register(Order)
admin.site.register(Postuplenie)
admin.site.register(PublicOffer)
admin.site.register(Payment)

