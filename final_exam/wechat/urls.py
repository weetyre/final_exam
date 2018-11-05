from django.urls import path
from . import views

urlpatterns = [
    path('login', views.index_login, name='login'),
    path('', views.index_me),
    path('me', views.index_me, name='me'),
    path('register', views.index_register, name='register'),
    path('logout', views.index_logout, name='logout')

]