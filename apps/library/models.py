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
    

class Izdatel(models.Model):
    name = models.CharField(max_length=80, verbose_name='name')
    adress = models.CharField(max_length=200, verbose_name='adress', blank=True, null=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    
    def __str__(self):
        return self.name


class Book(models.Model):         
    name = models.CharField(max_length=100, verbose_name='name')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True, null=True, related_name='book_author',
                               verbose_name='author')
    jenre = models.ManyToManyField(Jenre, related_name='book_jenre', verbose_name='jenre')
    description = models.TextField(verbose_name='text')
    avatar = models.ImageField(upload_to='books_avatar/')
    short_book_file = models.FileField(upload_to='books/')
    book_file = models.FileField(upload_to='books/', verbose_name='book')
    izdatel = models.ForeignKey(Izdatel, on_delete=models.SET_NULL,  blank=True, null=True, related_name='book_izdatel',
                                verbose_name='izdatel')
    year_izdat = models.DateField(verbose_name='year-izdat')
    amount_pages = models.IntegerField(validators=[MaxValueValidator(9999)], verbose_name='amount_pages')
    rating = models.FloatField(default=0, verbose_name='rating')
    cover_image = models.ImageField(upload_to='book_covers/')
    
    def __str__(self):
        return self.name
    

class Comment(models.Model):
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comment_book',
                                verbose_name='id_book')
    id_customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_customer',
                                    verbose_name='id_customer')
    comment = models.TextField(verbose_name='text')
    date = models.DateField(verbose_name='date', auto_now_add=True)
    
    def __str__(self):
        return self.id
    
    
