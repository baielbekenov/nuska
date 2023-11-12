from django.db import models
from django.core.validators import MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from apps.authentication.models import User

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='first')
    last_name = models.CharField(max_length=30, verbose_name='last_name')
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Jenre(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    

class Book(models.Model):         
    name = models.CharField(max_length=100, verbose_name='name')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True, null=True, related_name='book_author',
                               verbose_name='author')
    jenre = models.ManyToManyField(Jenre, related_name='book_jenre', verbose_name='jenre')
    description = models.TextField(verbose_name='text')
    avatar = models.ImageField(upload_to='books_avatar/', blank=True, null=True)
    short_book_file = models.FileField(upload_to='books/', blank=True, null=True)
    book_file = models.FileField(upload_to='books/', verbose_name='book', blank=True, null=True)
    created_at = models.DateField(default='2022-09-09')
    amount_pages = models.IntegerField(validators=[MaxValueValidator(9999)], verbose_name='amount_pages')
    rating = models.FloatField(default=0, verbose_name='rating')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    

class Comment(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments',
                                verbose_name='book_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user',
                                    verbose_name='user_id', blank=True, null=True)
    comment = models.TextField(verbose_name='text')
    date = models.DateField(verbose_name='date', auto_now_add=True)
    
    def __str__(self):
        return self.comment
    
    
