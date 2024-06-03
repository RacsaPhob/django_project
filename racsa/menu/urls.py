from django.urls import path
from django.views.decorators.cache import cache_page
from . import  views

urlpatterns = [
    path('',views.index.as_view(),name = 'menu'),
    path('detail/<str:name>/',views.menu_detailed.as_view(), name = 'detail'),
    path('<str:name>/',views.menu_category.as_view(), name = 'cat'),
    path('ajax', views.get_ajax,name='ajax')


]