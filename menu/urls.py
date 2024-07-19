from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page
from . import  views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'menu',views.MenuViewSet)


urlpatterns = [
    path('',views.index.as_view(),name = 'menu'),
    path('detail/<str:name>/',views.menu_detailed.as_view(), name = 'detail'),
    path('<str:name>/',views.menu_category.as_view(), name = 'cat'),
    path('ajax', views.get_ajax,name='ajax'),
    path('api/v1/',include(router.urls)),
    path(r'api/v1/auth', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),



]