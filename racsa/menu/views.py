from django.shortcuts import  get_object_or_404,HttpResponse,render
from .models import Menu, category
from django.views.generic import DetailView, ListView
from django.http import Http404
from django.http import JsonResponse


class index(ListView):
    paginate_by = 4

    template_name = 'menu/index.html'
    model = Menu
    context_object_name = 'menu'  # Это имя переменной, в которой находятся объекты с пагинацией

    def get_queryset(self):
        category_name = self.request.GET.get('category')


        if category_name !='all':
            data = Menu.objects.filter(cat__value=category_name)
            if len(data) == 0:
                raise Http404
            else:
                return data
        else:
            return Menu.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cats = category.objects.all()
        context['cats'] = cats
        context['curent_cat'] = self.request.GET.get('category')
        return  context

class menu_detailed(DetailView):
    model = Menu
    template_name = 'menu/detailed_view.html'
    context_object_name = 'coffee'



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        prev = self.request.GET.get('prev')
        print(prev)
        context['prev'] = prev


        return context
    def get_object(self, queryset=None):
        name = self.kwargs.get('name')  # в self.kwargs содержатся аргументы переданные при создании urlpattern

        return  get_object_or_404(Menu,name = name) #если в бд нет записей с таким значением параметра то будет 404

class menu_category(DetailView):
    model = category
    template_name = 'menu/index.html'
    context_object_name = 'category'

    def get_object(self, queryset=None):
       name = self.kwargs.get('name')
       return  get_object_or_404(category,value = name)

def get_ajax(request):

    cat = request.GET.get('cat')
    menu = Menu.objects.filter(cat__value=cat)

    result = list(menu.values('name','price','image'))
    for k, i in enumerate(menu):
        result[k]['image'] = i.image.url
        result[k]['link'] = i.get_absolute_url()
    print(result)
    return JsonResponse({'items': result},status=200)
