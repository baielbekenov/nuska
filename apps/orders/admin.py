from django.contrib import admin
from apps.orders.models import Order, Postuplenie, PublicOffer, Payment, Banner

# Register your models here.

admin.site.register(PublicOffer)
admin.site.register(Payment)
admin.site.register(Banner)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'order_date', 'order_status', 'total_sum')
    search_fields = ('book__name', 'user__email')
    list_filter = ['order_status']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(book__name__icontains=search_term)
            queryset |= self.model.objects.filter(user__email__icontains=search_term)
        return queryset, use_distinct


@admin.register(Postuplenie)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('book', 'date', 'cost', 'price', 'created_date')
    search_fields = ('book__name', )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(book__name__icontains=search_term)
        return queryset, use_distinct

