from django.urls import path
from . import views

urlpatterns = [
    path('login', views.index_login, name='login'),
    path('', views.index_profile),
    path('profile', views.index_profile, name='me'),
    path('register', views.index_register, name='register'),
    path('logout', views.index_logout, name='logout')

]