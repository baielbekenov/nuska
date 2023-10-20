from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from project.models import Order, Postuplenie, Soglashenie, User, Author, Jenre, Izdatel, Book, Customer, Comment


# class UserAdmin(TranslationAdmin):
#     pass


# class SoglashenieAdmin(TranslationAdmin):
#     pass


# class AuthorAdmin(TranslationAdmin):
#     pass


# class JenreAdmin(TranslationAdmin):
#     pass


# class IzdatelAdmin(TranslationAdmin):
#     pass


# class BookAdmin(TranslationAdmin):
#     pass


admin.site.register(User)
admin.site.register(Soglashenie)
admin.site.register(Author)
admin.site.register(Jenre)
admin.site.register(Izdatel)
admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Postuplenie)
admin.site.register(Comment)
