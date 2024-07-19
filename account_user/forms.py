from .models import user
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from allauth.account.forms import SignupForm, LoginForm


class AuthForm(SignupForm):
    """Класс формы для регистрации аккаунта """
    username = forms.CharField(label='имя', max_length=50, min_length=2)

    def __init__(self, *args, **kwargs):
        """Переопределяем атрибуты полей и полностью переопределяем поле email, т.к. в
            этом классе это поле генерируется само в момент инициализации и переопределяет
            то что определяли в атрибутах класса раннее"""

        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.pop('placeholder', None)
            field.widget.attrs['class'] = 'field'

        self.fields['email'] = forms.EmailField(label='эл.почта', required=True, max_length=255)



    def clean(self):
        username = self.cleaned_data.get('username')
        first_name = self.cleaned_data.get('first_name')
        if username == first_name:
            self.add_error('username', forms.ValidationError('username and first name must be different'))
        super().clean()


class Log_inForm(LoginForm):
    """
        Класс формы для входа в аккаунт
        по дефолту есть поле 'запомнить меня',
        убираем его
    """
    remember = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'remember' in self.fields:
            del self.fields['remember']

        for field_name, field in self.fields.items():
            field.widget.attrs.pop('placeholder', None)
            field.widget.attrs['class'] = 'field'

    def clean(self):

        self.cleaned_data['remember'] = True    #класс требует значение этого удалённого поля
        super().clean()


class UpdateUserForm(UserChangeForm):

    password_valid = forms.CharField(max_length=100, label='введите пароль', widget= forms.PasswordInput)
    password = None

    class Meta:
        model = user
        fields = ['username', 'email', 'avatar','password_valid']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'ava'}),
            'password_valid': forms.PasswordInput(attrs={'id': 'password_valid'})
        }