from django.contrib import admin
from apps.library.models import Author, Jenre, Book, Comment


admin.site.register(Author)
admin.site.register(Jenre)
admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    resource_class = Book
    fieldsets = (
        ("general", {"fields": ("name", "author", "jenre")}),
        ("other", {"fields": ("created_at", "rating", "isbn", "published_on")}),
    )
    list_filter = ("title",)

    # Render filtered options only after 5 characters were entered
    filter_input_length = {
        "title": 5,
    }
admin.site.register(Comment)
