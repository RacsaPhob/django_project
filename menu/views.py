from django.shortcuts import  get_object_or_404,HttpResponse,render
from .models import Menu, category, ShoppingCart, purchase
from django.views.generic import DetailView, ListView, TemplateView
from django.http import Http404
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import MenuSerializer
from  rest_framework.views import APIView
from django.forms import  model_to_dict
from rest_framework import generics

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

        if self.request.user.is_authenticated:
            cart, _ = ShoppingCart.objects.get_or_create(customer=self.request.user)
            purchases = cart.purchase_set.all()
        else:
            cart = None
            purchases = None

        context['cats'] = cats
        context['current_cat'] = self.request.GET.get('category')
        context['cart'] = cart
        context['purchases'] = purchases
        return  context

class menu_detailed(DetailView):
    model = Menu
    template_name = 'menu/detailed_view.html'
    context_object_name = 'coffee'



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        prev = self.request.GET.get('prev')
        context['prev'] = prev


        return context
    def get_object(self, queryset=None):
        name = self.kwargs.get('name')  # в self.kwargs содержатся аргументы переданные при создании urlpattern

        return  get_object_or_404(Menu,name = name) #если в бд нет записей с таким значением параметра, то будет 404

class menu_category(DetailView):
    model = category
    template_name = 'menu/index.html'
    context_object_name = 'category'

    def get_object(self, queryset=None):
       name = self.kwargs.get('name')
       return  get_object_or_404(category,value = name)

def get_ajax(request):
    """View для ajax запроса. Изменяет количество товара в корзине клиента"""

    pk = request.GET.get('pk')
    action = request.GET.get('action')

    purch_obj, is_created_or_deleted = _get_purch_obj(request.user,pk)
    purch_item = purch_obj.item
    if action == 'plus':
        if not is_created_or_deleted:
            purch_obj.amount +=1
            purch_obj.save()

    elif action == 'minus':
        purch_obj.amount -=1

        if purch_obj.amount == 0:
            purch_obj.delete()
            is_created_or_deleted = True

        else:
            purch_obj.save()
    else:
        is_created_or_deleted = True
        purch_obj.delete()


    return JsonResponse(data={'amount': purch_obj.amount,
                        'new_cost': purch_obj.get_full_price(discount=False),
                        'new_cost_with_discount': purch_obj.get_full_price(),
                        'name': purch_item.name,
                        'total_price':  purch_obj.cart.get_total_price(),
                        'is_created_or_deleted': is_created_or_deleted}
                        ,status=200)




class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

    def get_queryset(self):
        return Menu.objects.filter(cat_id=1)


def _get_purch_obj(user,pk) :
    cart = ShoppingCart.objects.get(customer=user)
    purchases = purchase.objects.filter(cart=cart)
    return purchases.get_or_create(item_id=pk, cart_id=cart.id)

