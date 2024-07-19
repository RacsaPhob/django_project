from .models import  reviews
from django import  forms

from captcha.fields import CaptchaField

class reviewsForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:

        model = reviews
        fields = ['text','captcha']



