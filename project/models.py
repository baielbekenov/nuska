from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    whois = models.CharField(max_length=150)
    access = models.CharField(max_length=150)
    acceptance = models.CharField(max_length=150)
    sogl = models.BooleanField()
    
    def __str__(self):
        return self.username
    
    
class Soglashenie(models.Model):
    name = models.CharField(max_length=150)
    text = models.TextField()
    date_created = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name
    


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
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=300, verbose_name='address', blank=True, null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
   
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
    

class Order(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL,  blank=True, null=True, verbose_name='id_user')
    id_book = models.ForeignKey(Book, on_delete=models.SET_NULL,  blank=True, null=True, verbose_name='id_book')
    
    order_date = models.DateField(verbose_name='date of order')
    order_status = models.BooleanField(verbose_name='status of order')
    totall_summ = models.DecimalField(decimal_places=2, max_digits=8)
    status_payment = models.BooleanField()
    
    
    
    def __str__(self):
        return self.id_user
    

class Postuplenie(models.Model):
    id_book = models.ForeignKey(Book, on_delete=models.SET_NULL,  blank=True, null=True, related_name='postu_book')
    date = models.DateField(auto_now_add=True)
    cost = models.DecimalField(decimal_places=2, max_digits=8)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    
    

class Comment(models.Model):
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comment_book',
                                verbose_name='id_book')
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comment_customer',
                                    verbose_name='id_customer')
    comment = models.TextField(verbose_name='text')
    date = models.DateField(verbose_name='date', auto_now_add=True)
    
    def __str__(self):
        return self.id
    



