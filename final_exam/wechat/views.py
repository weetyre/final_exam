from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from .admin import UserCreationForm
from .forms import LoginForm, RegisterForm, ChangeEmailForm
from .models import MyUser


def index_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            #if email is not found
            flag = 1
            user_model = MyUser.objects.all()
            for i in user_model:
                if i.email == email:
                    flag = 0

            if flag :
                error_message = 'email not found.'
                return render(request, 'login.html',
                              {'form': form, 'input_error': error_message, 'block_title': 'Login'})


            user = auth.authenticate(request, email=email, password=password)
            #incorrect password
            if user is None:
                error_message = 'password is invalid.'
                return render(request, 'login.html',
                              {'form': form, 'input_error': error_message, 'block_title': 'Login'})




            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                return HttpResponseRedirect("/profile")
                # Redirect to a success page.
            else:
                error_message = "Sorry, that's not a valid username or password"
                return render(request, 'login.html',
                              {'form': form, 'input_error': error_message, 'block_title': 'Login'})
    else:
        form = LoginForm()
    return render(request, 'login.html',
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

                return HttpResponseRedirect("/profile")
            else:
                error_message = 'The email is already taken'
                return render(request, 'register.html',
                              {'form': form, 'input_error': error_message, 'block_title': 'Register'})
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form, 'block_title': 'Register'})


def index_landingPage(request):
    #mainpage
    return render(request, 'landingpage.html')


@login_required
def index_profile(request):
    if request.method == 'GET':
        user = auth.authenticate(request)
        form1 = PasswordChangeForm(user=user)
        form2 = ChangeEmailForm()
        return render(request, 'settings_account.html',
                      {'user': user, 'form_change_psw': form1, 'form_change_email': form2})


@login_required
def index_logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")
