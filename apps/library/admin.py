from django.contrib import admin
from apps.library.models import Author, Jenre, Book, Comment


admin.site.register(Author)
admin.site.register(Jenre)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'jenre') 
    search_fields = ('name', 'author__name')
    
    def jenre(self, obj):
        """Возвращает строку со всеми жанрами книги."""
        return ', '.join([genre.name for genre in obj.jenre.all()])
    jenre.short_description = 'Жанрлар'
    
    
admin.site.register(Comment)
