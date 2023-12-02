from django.contrib import admin


class JenreFilter(admin.SimpleListFilter):
    title = 'Жанр'
    parameter_name = 'jenre'

    def lookups(self, request, model_admin):
        jenres = set([jenre for book in model_admin.model.objects.all() for jenre in book.jenre.all()])
        return [(jenre.id, jenre.name) for jenre in jenres]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(jenre__id__exact=self.value())
        return queryset