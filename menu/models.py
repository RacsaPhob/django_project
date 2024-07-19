from django.db import models
from django.urls import reverse
from account_user.models import user
from django.core.exceptions import ValidationError


class Menu(models.Model):
    name = models.CharField('наименование', max_length=50)
    price = models.DecimalField('цена', max_digits=10, decimal_places=2)
    description = models.TextField('описание', max_length=500)
    cat = models.ForeignKey('category', on_delete=models.PROTECT, verbose_name='категория', null=True)
    image = models.ImageField('фото', upload_to='images/menu')
    quantity = models.IntegerField('количество',default=1)

    discount = models.DecimalField('скидка в $',default=0,decimal_places= 2,max_digits=10)
    percent_discount = models.PositiveSmallIntegerField(verbose_name='скидка в процентах',default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'name': self.name})

    def get_price_with_discount(self):
        return self.price - self.discount


    def save(self, *args,**kwargs):
        if self.discount and not(self.percent_discount):
            self.percent_discount = round((self.discount / self.price) * 100)

        if self.percent_discount and not self.discount:
            self.discount = self.price * self.percent_discount / 100

        if self.price <= self.discount:
            raise ValidationError('discount is more than price')

        super().save(args,kwargs)

    class Meta:
        verbose_name = 'меню'
        verbose_name_plural = 'меню'
        ordering = ['pk']


class category(models.Model):
    value = models.CharField('категория', max_length=50)
    image = models.ImageField('фото', upload_to='images/categories')

    def __str__(self):
        return self.value

    def get_absolute_url(self):
        return reverse('cat', kwargs={'name': self.value})



class purchase(models.Model):
    item = models.ForeignKey(Menu,verbose_name='товар', null=False,on_delete=models.CASCADE)
    amount = models.PositiveIntegerField('количество',default=1)
    cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE,verbose_name='в корзине')


    def get_full_price(self,discount=True):
        if discount:
            return self.amount * (self.item.price - self.item.discount)
        else:
            return self.amount * self.item.price

class ShoppingCart(models.Model):
    customer = models.OneToOneField(user,on_delete=models.CASCADE, verbose_name='покупатель', null=False)
    status = models.IntegerField('статус',default=1)

    def get_total_price(self):
        print(sum([pur.get_full_price() for pur in self.purchase_set.all()]))
        return sum([pur.get_full_price() for pur in self.purchase_set.all()])



