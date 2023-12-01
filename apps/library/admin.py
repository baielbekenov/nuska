from django.contrib import admin
from apps.library.models import Author, Jenre, Book, Comment


admin.site.register(Author)
admin.site.register(Jenre)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author') 
admin.site.register(Comment)
