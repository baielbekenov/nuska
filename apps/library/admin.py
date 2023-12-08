from django.contrib import admin
from apps.library.models import Author, Jenre, Book, Comment
from apps.library.modelfilter import  JenreFilter
import xlwt
from django.http import HttpResponse

admin.site.register(Author)
admin.site.register(Jenre)


def export_as_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Book")

    row_num = 0
    columns = [field.name for field in modeladmin.model._meta.fields]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num])

    for obj in queryset:
        row_num += 1
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, getattr(obj, columns[col_num]))

    wb.save(response)
    return response

export_as_excel.short_description = "Export Selected"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'display_jenres')
    search_fields = ('name', )
    list_filter = (JenreFilter,)
    actions = [export_as_excel]

    def display_jenres(self, obj):
        """Возвращает строку со всеми жанрами книги."""
        return ', '.join([genre.name for genre in obj.jenre.all()])
    display_jenres.short_description = 'Жанрлар'
    
    
admin.site.register(Comment)
