from django.contrib import admin
from apps.library.models import Author, Jenre, Book, Comment
from apps.library.modelfilter import JenreFilter
from import_export.admin import ImportExportModelAdmin

admin.site.register(Author)
admin.site.register(Jenre)

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'display_author', 'display_jenres')
    search_fields = ('name', )
    list_filter = (JenreFilter,)

    def display_jenres(self, obj):
        """Возвращает строку со всеми жанрами книги."""
        return ', '.join([genre.name for genre in obj.jenre.all()])
    display_jenres.short_description = 'Жанрлар'

    def display_author(self, obj):
        return ', '.join([f"{author.first_name} {author.last_name}" for author in obj.author.all()])

    display_author.short_description = 'Авторлор'

    
admin.site.register(Comment)
