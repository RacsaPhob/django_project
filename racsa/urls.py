from django.conf import  settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'),name = 'main'),
    path('menu/',include('menu.urls')),
    path('captcha/', include('captcha.urls')),
    path('accounts/', include('account_user.urls')),
    path('accounts/', include('allauth.urls')),


]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
