from django.shortcuts import render,redirect
from .models import reviews, user
from .forms import reviewsForm,AuthForm, log_inForm, UpdateUserForm
from django.views.generic import CreateView, UpdateView, ListView, FormView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout,login
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.urls import  reverse_lazy
def index(r):

    revs = reviews.objects.order_by('-pk')[0:8]

    return render(r,'main/index.html',{'revs':revs})

def about(r):

    return render(r,'main/about.html')


def contact(r):
    return  render(r,'main/contact.html')
@login_required
def add_review(r):
    if r.method == 'POST':

        form = reviewsForm(r.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = r.user
            review.save()
            return redirect('/')

    form = reviewsForm()

    data = {'form':form}
    return  render(r,'main/add_review.html',data)

def log_out(r):
    logout(r)
    return redirect('/')

def get_ajax(request):
    passw = request.GET.get('passw')
    if request.user.check_password(passw):
        return JsonResponse({'validate': True}, status=200)
    else:
        return JsonResponse({'validate': False}, status=200)


class auth(CreateView):
    template_name = 'main/auth.html'
    form_class = AuthForm
    success_url = reverse_lazy('auth')

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('/')

class log_in(LoginView):
    form_class = log_inForm
    template_name = 'main/log_in.html'


class account(LoginRequiredMixin,ListView):
    template_name = 'main/account.html'
    model = user

class account_edit(LoginRequiredMixin, FormView):
    template_name = 'main/account_edit.html'
    form_class = UpdateUserForm

    def form_valid(self, form):
        passw = self.request.POST['password_valid']

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




