from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from account_app.admin import UserCreationForm
from account_app.forms import LoginForm, RegisterForm
from account_app.models import MyUser


def index_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("me?user=" + username)
            else:
                error_message = "Sorry, that's not a valid username or password"
                return render(request, 'account_app/login.html',
                              {'form': form, 'input_error': error_message, 'block_title': 'Login'})
    else:
        form = LoginForm()
    return render(request, 'account_app/login.html',
                  {'form': form, 'block_title': 'Login'})


def index_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_filter = MyUser.objects.filter(email=request.POST['email'])
            if len(user_filter) <= 0:
                form.save()
                username = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = auth.authenticate(request, username=username, password=password)
                auth.login(request, user)

                return HttpResponseRedirect("/me")
            else:
                error_message = 'The email is already taken'
                return render(request, 'account_app/register.html',
                              {'form': form, 'input_error': error_message, 'block_title': 'Register'})
    else:
        form = UserCreationForm()
    return render(request, 'account_app/register.html', {'form': form, 'block_title': 'Register'})


@login_required
def index_me(request):
    user = auth.authenticate(request)
    return render(request, 'account_app/me.html', user)


@login_required
def index_logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")
