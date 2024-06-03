from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField('наименование', max_length=50)
    price = models.DecimalField('цена', max_digits=10, decimal_places=2)
    description = models.TextField('описание', max_length=500)
    cat = models.ForeignKey('category', on_delete=models.PROTECT, verbose_name='категория', null=True)
    image = models.ImageField('фото', upload_to='images/menu')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'name': self.name})

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
