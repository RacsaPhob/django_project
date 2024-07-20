
from django.shortcuts import redirect, render, HttpResponse
from .models import user
from .forms import AuthForm, Log_inForm, UpdateUserForm
from django.views.generic import ListView, FormView, TemplateView, View
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from allauth.account.views import SignupView, LoginView
from .utils import get_google_service_url, get_google_user, create_user_by_google_info


def log_out(r):
    logout(r)
    return redirect('/')


def get_ajax(request):
    passw = request.GET.get('passw')
    if request.user.check_password(passw):
        return JsonResponse({'validate': True}, status=200)
    else:
        return JsonResponse({'validate': False}, status=200)


@login_required()
def account_delete_view(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('/')

    return render(request, template_name='account/delete.html')


class Login(LoginView):
    form_class = Log_inForm
    template_name = 'account/log_in.html'


class Account(LoginRequiredMixin, ListView):
    template_name = 'account/account.html'
    model = user


class AccountEdit(LoginRequiredMixin, FormView):
    template_name = 'account/account_edit.html'
    form_class = UpdateUserForm

    def form_valid(self, form):

        passw = self.request.POST.get('password_valid')
        if self.request.user.check_password(passw):
            form.save()
            return redirect('account')
        else:
            form.add_error('password_valid', 'Неверный пароль')
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user  # Передаем текущего пользователя в качестве экземпляра формы
        return kwargs


class AuthView(SignupView):
    template_name = 'account/auth.html'
    form_class = AuthForm

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)


class AccountGoogleView(TemplateView):
    template_name = 'account/google.html'

    def get(self, request, *args, **kwargs):
        link = get_google_service_url(request)
        return redirect(link)


class GoogleCallback(View):
    def get(self, request, *args, **kwargs):
        self.state_validation(request)

        google_user_info = get_google_user(request)
        new_user = create_user_by_google_info(google_user_info, user)
        login(request, new_user)

        return redirect('/')

    def state_validation(self, request):
        """Проверка CSRF токенов переданных через GET запрос и через сессию"""

        state_get = request.GET.get('state')
        state_session = request.session.get('oauth_state')

        if state_get != state_session:
            raise PermissionDenied('invalid CSRF token')

        del request.session['oauth_state']
