from django.urls import path, include
from . import  views


from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('',views.index, name = 'main'),
    path('about',views.about),
    path('contacts',views.contact),
    path('add_review',views.add_review),
    path('auth',views.auth.as_view(),name = 'auth'),
    path('log_in',views.log_in.as_view(),name = 'log_in'),
    path('log_out',views.log_out,name = 'log_out'),
    path('account/edit',views.account_edit.as_view(),name = 'account_edit'),
    path('account',views.account.as_view(),name = 'account'),
    path('password-reset/', PasswordResetView.as_view(template_name='main/reset_password.html'), name = 'password_reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('password-reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='main/reset_password.html'),name = 'password_reset_confirm'),
    path('password-reset/complete', PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path('account/ajax', views.get_ajax, name = 'ajax')

]