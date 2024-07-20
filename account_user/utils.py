import secrets
import string

from django.conf import settings
from allauth.socialaccount.models import SocialApp
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist


from requests_oauthlib import OAuth2Session


def get_google_service_url(request):
    """
        Функция для получения url для google accounts, там где пользователь
        может выбрать google account для входа на сайт
    """

    google_session = get_oauth_session(SocialApp.objects.get(name='google'))
    authorization_url, state = get_authorization_url_and_state(google_session)

    # Сохраните состояние в сессии, чтобы проверить его после
    request.session['oauth_state'] = state
    return authorization_url


def get_oauth_session(google, state=None, scope=True):
    """Возвращает OAuth сессию, принимает объект google из модели SocialApp"""

    if scope:
        scope = settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE']
    else:
        scope = None
    return OAuth2Session(google.client_id,
                         redirect_uri='https://127.0.0.1:8000/accounts/google/login/callback/',
                         scope=scope,
                         state=state
                         )


def get_authorization_url_and_state(session):
    """Возвращает готовый url, где пользователь может выбрать google аккаунт для входа"""
    return session.authorization_url(
        'https://accounts.google.com/o/oauth2/auth',
        access_type="offline",  # получить refresh токен тоже
        prompt="select_account")    # у пользователя всегда будет возможность выбрать google аккаунт


def google_fetch_token(google_session, google_app, request):
    """Принимает google session и у него обменивает код из url на токен"""

    return google_session.fetch_token(
        'https://accounts.google.com/o/oauth2/token',
        client_secret=google_app.secret,
        authorization_response=request.build_absolute_uri())  # полный uri текущей страницы(там находится code)


def get_google_user(request):
    """Создаёт новую сессию без scope, в этой сессии обменивает код на токен.
        Возвращает словарь с данными полученными от аккаунта google пользователя
        """

    google_app = SocialApp.objects.get(name='google')
    google_session = get_oauth_session(google_app, request.session.get('oauth_state'), scope=False)
    token = google_fetch_token(google_session, google_app, request)

    return google_session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()


def _get_state(length=16):
    """Генерирует случайную строку"""

    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def create_user_by_google_info(user_inf, user_model):
    """Создаёт пользователя с помощью полученной информации от google_api"""

    password = create_hashed_password(length=10)
    username = user_inf.get('name')
    given_name = user_inf.get('given_name')
    verified_email = user_inf.get('verified_email')

    if verified_email:
        email = user_inf.get('email')

    else:
        raise PermissionDenied('email is not verified')

    check_user = get_user_by_email_or_none(email, user_model)
    if check_user:
        if not check_user.first_name:
            check_user.first_name = given_name
            check_user.save()

        return check_user

    else:
        new_user, _ = user_model.objects.get_or_create(
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


def get_user_by_email_or_none(email, user_model):
    """Проверяет есть ли пользователь с таким email в бд"""

    try:
        return user_model.objects.get(email=email)
    except ObjectDoesNotExist:
        return None
