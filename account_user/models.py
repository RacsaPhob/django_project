from django.db import models
from django.contrib.auth.models import AbstractUser


class user(AbstractUser):
    balance = models.DecimalField('баланс',max_digits=9,decimal_places=2,default=0.0)
    avatar = models.ImageField('аватарка',default='images/anonimus_user.png',upload_to='images/users/')


