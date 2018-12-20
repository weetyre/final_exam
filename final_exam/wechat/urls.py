from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.index_login, name='login'),
    path('', views.index_landingPage),
    path('profile', views.index_profile, name='profile'),
    path('register', views.index_register, name='register'),
    path('logout', views.index_logout, name='logout'),
    path('account/change_psw', views.account_psw_change, name='change_psw'),
    path('account/change_email', views.account_email_change),
    path('account/create_group', views.create_group),
    path('account/add_group', views.add_group),
    path('account/add_friends', views.add_friends),
    path('home', views.myhome),
    path('add', views.add),
    url(r'^echo/(?P<userid>[0-9]+)$', views.echo, name='echo'),
    url(r'get-history-msg', views.get_mes, name='mes')
]
