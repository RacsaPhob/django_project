from django.shortcuts import render,redirect
from .models import reviews
from .forms import reviewsForm
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from  django.contrib.auth.mixins import LoginRequiredMixin

def index(r):
    revs = reviews.objects.order_by('-pk')[0:8]

    return render(r,'main/index.html',{'revs':revs})

def about(r):
    return render(r,'main/about.html')


def contact(r):
    return  render(r,'main/contact.html')
class add_review(LoginRequiredMixin,CreateView):
    form_class = reviewsForm
    template_name = 'main/add_review.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class review_detailed(LoginRequiredMixin,DetailView,UpdateView):
    model = reviews
    template_name = 'main/review_detailed.html'
    context_object_name = 'review'
    form_class = reviewsForm

    def get_form_kwargs(self):
        self.object = self.get_object()
        if self.object.author == self.request.user:
            kwargs = super().get_form_kwargs()
            kwargs['instance'] = self.object  # Передаем текущего пользователя в качестве экземпляра формы
            return kwargs
        else:
            return self.handle_no_permission()


    def form_valid(self, form):

        form.save()
        return redirect('/')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'delete' in request.POST:
            return self.delete()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def delete(self):
        self.get_object().delete()
        return redirect('/')



