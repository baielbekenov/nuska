from django.db import models
from apps.authentication.models import User
from apps.library.models import Book
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='колдонуучу')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='китеп')
    order_date = models.DateField(auto_now_add=True, verbose_name='заказдын датасы')
    order_status = models.BooleanField(default=False, verbose_name='заказдын абалы')
    total_sum = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True, verbose_name='жалпы суммасы')

    def __str__(self):
        return f"{self.user} -- {self.book}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказдар'


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', verbose_name='заказ')
    amount = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='сумма')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='төлөөм датасы')
    status = models.CharField(max_length=30, choices=[
        ('processing', 'Иштетүү...'),
        ('completed', 'Аякталды'),
        ('failed', 'Ийгиликсиз'),
        ('refunded', 'Кайтты')
    ], default='processing', verbose_name='төлөм абалы')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='транзакция ID')

    def __str__(self):
        return f"Заказ {self.id} менен төлөө {self.order.id}"

    class Meta:
        verbose_name = 'Төлөм'
        verbose_name_plural = 'Төлөмдөр'
    

class Postuplenie(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL,  blank=True, null=True,
                             related_name='postu_book', )
    date = models.DateField(auto_now_add=True)
    cost = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    price = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.book)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.book:
            self.book.price = self.price
            self.book.save()
    
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


