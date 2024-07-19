from django.db import models
from django.urls import reverse
from account_user.models import user

class reviews(models.Model):
    author = models.ForeignKey(user,on_delete=models.PROTECT,null=True,verbose_name='автор')
    text = models.CharField('отзыв',max_length=250,help_text='напишите отзыв здесь')
    cat = models.ForeignKey('category',on_delete=models.PROTECT,null=True,verbose_name='тип')
    def __str__(self):
        return  self.author.username

    def get_absolute_url(self):
        return reverse('review_detailed', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

class category(models.Model):
    value = models.CharField(max_length=50,db_index=True)

    def __str__(self):
        return self.value

