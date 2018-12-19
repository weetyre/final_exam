from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from .admin import UserCreationForm
from .forms import LoginForm, ChangeEmailForm, MyPasswordChangeForm
from .models import MyUser
from django.db.models import Q
from django.contrib.auth import authenticate


def index_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            password = form.cleaned_data['password']

            # # if email is not found
            user_model = None
            try:
                user_model = MyUser.objects.get(email=text)
            except Exception as e:
                pass

            if user_model:
                user = authenticate(request=request, username=text, password=password)
                # incorrect password
                if user is None:
                    error_message = 'password is invalid.'
                    return render(request, 'login.html',
                                  {'form': form, 'input_error': error_message, 'block_title': 'Login'})
            else:
                try:
                    user_model = MyUser.objects.get(username=text)
                except Exception as e:
                    pass

                if user_model:
                    user = authenticate(request=request, username=text, password=password)
                    # incorrect password
                    if user is None:
                        error_message = 'password is invalid.'
                        return render(request, 'login.html',
                                      {'form': form, 'input_error': error_message, 'block_title': 'Login'})
                else:
                    error_message = 'email or username not found.'
                    return render(request, 'login.html',
                                  {'form': form, 'input_error': error_message, 'block_title': 'Login'})

            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                return HttpResponseRedirect("/home")
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

        email_filter = MyUser.objects.filter(email=request.POST['email'])
        username_filter = MyUser.objects.filter(username=request.POST['username'])
        if len(email_filter) <= 0 and len(username_filter) <= 0:
            # form.save()
            username = request.POST['username']
            email = request.POST['email']
            sex = request.POST['sex']
            # password = make_password(form.cleaned_data['password'])
            user = MyUser.objects.create_user(username=username, email=email, sex=sex,
                                              password=request.POST['password'])

            user = authenticate(request=request, username=email, password=request.POST['password'])
            auth.login(request, user)

            return HttpResponseRedirect("/home")
        else:
            if len(email_filter) > 0:
                error_msg1 = 'email already taken.'
                return render(request, 'register.html',
                              {'form': form, 'input_error2': error_msg1, 'block_title': 'Register'})

            if len(username_filter) > 0:
                error_msg2 = 'username already taken.'
                return render(request, 'register.html',
                              {'form': form, 'input_error': error_msg2, 'block_title': 'Register'})

    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form, 'block_title': 'Register'})


def index_landingPage(request):
    # mainpage
    return render(request, 'landingpage.html')


@login_required
def index_profile(request):
    if request.method == 'GET':
        user = request.user
        # user = auth.authenticate(request)
        form1 = MyPasswordChangeForm(user=user)
        form2 = ChangeEmailForm()
        return render(request, 'settings_account.html',
                      {'user': user, 'form_change_psw': form1, 'form_change_email': form2})


@login_required
def account_psw_change(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            form2 = ChangeEmailForm()

            msg = 'succeeded!'
            return render(request, 'settings_account.html',
                          {'user': request.user, 'form_change_psw': form,
                           'form_change_email': form2, 'success_msg1': msg})
        else:
            form2 = ChangeEmailForm()
            return render(request, 'settings_account.html',
                          {'user': request.user, 'form_change_psw': form, 'form_change_email': form2})


@login_required
def account_email_change(request):
    if request.method == 'POST':
        user = request.user
        email = request.POST['email']
        email_filter = MyUser.objects.filter(email=request.POST['email'])
        if len(email_filter) <= 0:
            user.email = email
            user.save()
            form1 = MyPasswordChangeForm(user=user)
            form2 = ChangeEmailForm()
            msg = 'succeeded!'
            return render(request, 'settings_account.html',
                          {'user': request.user, 'form_change_psw': form1,
                           'form_change_email': form2, 'success_msg2': msg})
        else:
            form1 = MyPasswordChangeForm(user=user)
            form2 = ChangeEmailForm()
            error_message = 'email already taken.'
            return render(request, 'settings_account.html',
                          {'user': user, 'form_change_psw': form1, 'form_change_email': form2,
                           'error_msg': error_message})


@login_required
def index_logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")


@login_required
def myhome(request):
    if request.method == 'GET':
        friends = [
            {'id': 1, 'name': 'van'},
            {'id': 1, 'name': 'dark'},
            {'id': 1, 'name': 'holmes'},
            {'id': 1, 'name': 'bili'},
            {'id': 1, 'name': 'bill'},
            {'id': 1, 'name': 'bilibili'},
            {'id': 1, 'name': 'kakasi'},
            {'id': 1, 'name': 'naruto'},
            {'id': 1, 'name': 'kanojo'},

        ]
        return render(request, 'home_base.html', {'user': request.user, 'friends': friends})


@login_required
def add(request):
    if request.method == 'GET':
        return render(request, 'add_friends.html', {'user': request.user})


class CustomBackend(ModelBackend):
    """邮箱也能登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MyUser.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
