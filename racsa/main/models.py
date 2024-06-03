from django.db import models
from django.contrib.auth.models import AbstractUser
class reviews(models.Model):
    author = models.ForeignKey('user',on_delete=models.PROTECT,null=True,verbose_name='автор')
    text = models.TextField('отзыв',max_length=250)
    cat = models.ForeignKey('category',on_delete=models.PROTECT,null=True,verbose_name='тип')
    def __str__(self):
        return  self.author.username

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

class category(models.Model):
    value = models.CharField(max_length=50,db_index=True)

    def __str__(self):
        return self.value

class user(AbstractUser):
    balance = models.DecimalField('баланс',max_digits=9,decimal_places=2,default=0.0)
    avatar = models.ImageField('аватарка',default='images/anonimus_user.png',upload_to='images/users')
