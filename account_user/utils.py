import urllib.parse
import secrets
import string
import requests

from django.conf import settings
from allauth.socialaccount.models import SocialApp
from .models import user
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist



def get_google_service_url(request):
    """
        Функция для получения url для google accounts, там где пользователь
        может выбрать google account для входа на сайт
    """

    base_url = 'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?'
    state = _get_state()
    request.session['oauth_state'] = state
    # создание GET параметров
    params = {
              'scope': _get_scopes(),
              'client_id': SocialApp.objects.get(name='google').client_id,
              'redirect_uri': 'http://127.0.0.1:8000/accounts/google/login/callback/',
              'response_type': 'code',
              'access_type': 'online',
              'flowName': 'GeneralOAuthFlow',
              'service': 'lso',
              'o2v': '2',
              'state': state
              }
    params_encoded = urllib.parse.urlencode(params)
    url_params_encoded = params_encoded.replace('+',  '%20')
    return base_url + url_params_encoded


def _get_scopes():
    """Возвращает строку со scopes разделенных пробелом"""

    scopes = ''
    for scope in settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE']:
        scopes += scope + ' '
    scopes = scopes[0:-1]

    return scopes


def _get_state(length=16):
    """Генерирует случайную строку"""

    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def exchange_code_for_token(code):
    """обменивает код полученный от google accounts на access token"""

    provider = SocialApp.objects.get(name='google')
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': provider.client_id,
        'client_secret': provider.secret,
        'redirect_uri': 'http://127.0.0.1:8000/accounts/google/login/callback/',
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=data)
    return response.json()


def get_user_inf(access_token):
    """Заходит на google api под именем пользователя и получает информацию о нем"""

    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(user_info_url, headers=headers)
    return response.json()


def create_user(user_inf):
    """Создаёт пользователя с помощью полученной информации от get_user_inf"""

    password = create_hashed_password(length=10)
    username = user_inf.get('name')
    given_name = user_inf.get('given_name')
    verified_email = user_inf.get('verified_email')

    if verified_email:
        email = user_inf.get('email')

    else:
        raise PermissionDenied('email is not verified')

    check_user = get_user_by_email_or_none(email=email)
    if check_user:
        if not check_user.first_name:
            check_user.first_name = given_name

        return check_user

    else:
        new_user, _ = user.objects.get_or_create(
                                                password=password,
                                                username=username,
                                                first_name=given_name,
                                                email=email
                                                )
        return new_user


def create_hashed_password(length):
    """Создаёт уникальный случайный пароль и возвращает хэшированный"""
    password = _get_state(length)
    print(password)
    return make_password(password)


def get_user_by_email_or_none(email):
    """Проверяет есть ли пользователь с таким email в бд"""

    try:
        return user.objects.get(email=email)
    except ObjectDoesNotExist:
        return None


def user_by_code(code):
    """Создаёт пользователя с помощью данный полученных от
        api google     """

    response = exchange_code_for_token(code)
    user_inf = get_user_inf(response['access_token'])
    new_user = create_user(user_inf)

    return new_user
