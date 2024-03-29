from django.db import models
from django.core.validators import MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from apps.authentication.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Аты')
    last_name = models.CharField(max_length=30, verbose_name='Фамилиясы')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='author', verbose_name='Автору')
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторлор'


class Jenre(models.Model):
    name = models.CharField(max_length=30, verbose_name='аталыш')
    
    def __str__(self):
        return self.name
    
    class Meta:
        
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанрлар'
    

class Book(models.Model):         
    name = models.CharField(max_length=100, verbose_name='китептин аталышы')
    author = models.ManyToManyField(Author, related_name='book_author', verbose_name='автору')
    jenre = models.ManyToManyField(Jenre, related_name='book_jenre', verbose_name='жанр')
    description = models.TextField(verbose_name='мазмуну')
    avatar = models.ImageField(upload_to='books_avatar/', blank=True, null=True, verbose_name='аватар')
    short_book_file = models.FileField(upload_to='books/', blank=True, null=True, verbose_name='кыскача китеп')
    book_file = models.FileField(upload_to='books/', verbose_name='китеп файлы', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='кошулган куну')
    amount_pages = models.IntegerField(validators=[MaxValueValidator(9999)], verbose_name='барактардын саны')
    sales_count = models.IntegerField(default=0, verbose_name='Сатылгандардын саны')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name='постер')
    active = models.BooleanField(default=True, verbose_name='активдүү')
    amount_view = models.IntegerField(default=0, verbose_name='көрүүлөрдүн саны')
    price = models.IntegerField(default=0, verbose_name='баасы')
    addres = models.CharField(max_length=90, verbose_name='дарек', blank=True, null=True)
    phone_number = models.IntegerField(max_length=10, verbose_name='телефон номуру', blank=True, null=True)
    ig_account = models.CharField(max_length=150, verbose_name='соц аккаунт', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        
        verbose_name = 'Китеп'
        verbose_name_plural = 'Китептер'

        # Default ordering of records
        ordering = ['-created_at']  # Orders by creation date, newest first

        # Any other meta options you want to include
        # For example, if you want to make sure that no two books have the same name and author
    

class Comment(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments',
                                verbose_name='китептин номери')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user',
                                    verbose_name='колдонуучунун номери', blank=True, null=True)
    comment = models.TextField(verbose_name='пикир')
    date = models.DateField(verbose_name='датасы', auto_now_add=True)
    
    def __str__(self):
        return self.comment
    
    
    class Meta:
        
        verbose_name = 'Пикир'
        verbose_name_plural = 'Пикирлер'


class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorited_by')
    added_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together =('user', 'book')
        verbose_name = 'Тандалган китеп'
        verbose_name_plural = 'Тандалган китептер'

    def __str__(self):
        return f"{self.user.email} - {self.book.name}"



    
    
