from django.contrib import admin
from apps.library.models import Author, Jenre, Book, Comment
from apps.library.modelfilter import  JenreFilter

admin.site.register(Author)
admin.site.register(Jenre)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'display_jenres')
    search_fields = ('name', )
    list_filter = (JenreFilter,)

    def display_jenres(self, obj):
        """Возвращает строку со всеми жанрами книги."""
        return ', '.join([genre.name for genre in obj.jenre.all()])
    display_jenres.short_description = 'Жанрлар'
    
    
admin.site.register(Comment)
