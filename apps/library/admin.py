from django.contrib import admin
from apps.library.models import Author, Jenre, Izdatel, Book, Comment


admin.site.register(Author)
admin.site.register(Jenre)
admin.site.register(Izdatel)
admin.site.register(Book)
admin.site.register(Comment)
