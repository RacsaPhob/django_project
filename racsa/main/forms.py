from .models import  reviews, user
from django import  forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from captcha.fields import CaptchaField

class reviewsForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:

        model = reviews
        fields = ['text','captcha']


class AuthForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Введенные пароли не совпадают.",
        'password_too_short': 'длина пароля должна быть 6 или более символов'

    }
    username = forms.CharField(label='asdsd')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        elif password2 and len(password2) < 6 :
            raise forms.ValidationError(
                self.error_messages['password_too_short'],
                code='password_too_short',)
        return password2
    class Meta:
        model = user
        fields = ('username','password1','password2','email','first_name','last_name',)
        widgets = {
            'username':forms.TextInput(attrs={'id': 'username'})
        }

class log_inForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Неправильный логин или пароль. Пожалуйста, попробуйте снова."
    }

class UpdateUserForm(UserChangeForm):
    password = None
    password_valid = forms.CharField(max_length=100, label='введите пароль', widget= forms.PasswordInput)

    class Meta:
        model = user
        fields = ['username', 'email', 'avatar','password_valid']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'ava'}),
            'password_valid' : forms.PasswordInput(attrs={'id': 'password'})
        }



