from django.urls import path
from . import  views

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [path('signup/',views.Auth_View.as_view(),name = 'auth'),
    path('login/',views.log_in.as_view(),name = 'log_in'),
    path('logout/',views.log_out,name = 'log_out'),
    path('edit',views.account_edit.as_view(),name = 'account_edit'),
    path('',views.account.as_view(),name = 'account'),
    path('delete/',views.Account_deleteView, name='account_delete'),
    path('google/login/',views.Account_GoogleView.as_view(), name='account_google'),
    path('google/login/callback/',views.Google_callback.as_view(), name='google_callback'),
    path('password-reset/', PasswordResetView.as_view(template_name='main/reset_password.html'), name = 'password_reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('password-reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='main/reset_password.html'),name = 'password_reset_confirm'),
    path('password-reset/complete', PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path('ajax', views.get_ajax, name = 'ajax'),

]