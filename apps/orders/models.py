from django.db import models
from apps.authentication.models import User
from apps.library.models import Book

# Create your models here.


class Order(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL,  blank=True, null=True, verbose_name='id_user')
    id_book = models.ForeignKey(Book, on_delete=models.SET_NULL,  blank=True, null=True, verbose_name='id_book')
    
    order_date = models.DateField(verbose_name='date of order')
    order_status = models.BooleanField(verbose_name='status of order')
    totall_summ = models.DecimalField(decimal_places=2, max_digits=8)
    status_payment = models.BooleanField()
    
    def __str__(self):
        return self.id_user
    
    class Meta:
        
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказдар'
    

class Postuplenie(models.Model):
    id_book = models.ForeignKey(Book, on_delete=models.SET_NULL,  blank=True, null=True, related_name='postu_book')
    date = models.DateField(auto_now_add=True)
    cost = models.DecimalField(decimal_places=2, max_digits=8)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    
    def __str__(self):
        return str(self.id_book)
    
    class Meta:
        
        verbose_name = 'Келгендер'
        verbose_name_plural = 'Келгендер'


class PublicOffer(models.Model):
    title = models.CharField(max_length=200, verbose_name='Аталыш')
    content = models.TextField(verbose_name='Мазмуну')
    is_active = models.BooleanField(default=True, verbose_name='Жанык')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Публичное предложение'
        verbose_name_plural = 'Публичные предложения'


