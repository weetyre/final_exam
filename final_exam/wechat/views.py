from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
import sqlite3
from .admin import UserCreationForm
from .forms import LoginForm, ChangeEmailForm, MyPasswordChangeForm
from .models import MyUser
from . import models
from django.db.models import Q
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from dwebsocket.decorators import accept_websocket, require_websocket
from collections import defaultdict
import json
from flask import Flask, render_template, request, jsonify

# 保存所有接入的用户地址
allconn = defaultdict(list)


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
        user = request.user
        friends = selectFrinds(user.username)

        return render(request, 'home_base.html', {'user': user, 'friends': friends})


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


@accept_websocket
def echo(request, userid):
    allresult = {}
    # 获取用户信息
    userinfo = request.user
    allresult['userinfo'] = userinfo
    # 声明全局变量
    global allconn
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index.html', allresult)
    else:
        # 将链接(请求？)存入全局字典中
        allconn[str(userid)] = request.websocket
        # 遍历请求地址中的消息
        for message in request.websocket:
            # 将信息发至自己的聊天框
            request.websocket.send(message)
            mes = json.loads(message)
            models.One_to_one_msg_record.objects.create(form_id_id=mes['from'], to_id_id=int(mes['to']),content=mes['msg'])
            # 将信息发至其他所有用户的聊天框
            for i in allconn:
                if i != str(userid):

                    allconn[i].send(message)


# 查找myuser表，通过用户的name，返回用户id
def selectuid(uname):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    # userid = cursor.execute('select id from wechat_myuser where username = uname')
    # values = cursor.execute('select friend_id from wechat_user_realation where uid = ?',('value1',))
    cursor = conn.execute("SELECT id, username  from wechat_myuser")
    for row in cursor:
        if (row[1] == uname):
            uuid = row[0]
            print(uuid)
    conn.close()
    return uuid


# 根据id 返回name

def selectuname(uid):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    # userid = cursor.execute('select id from wechat_myuser where username = uname')
    # values = cursor.execute('select friend_id from wechat_user_realation where uid = ?',('value1',))
    cursor = conn.execute("SELECT id, username  from wechat_myuser")
    for row in cursor:
        if (row[0] == uid):
            uname = row[1]
    conn.close()
    return uname


# 好友关系表
# 根据id，返回用户的所有的好友name 数组？
def selectFrinds(uname):
    # 该用户的id
    uuuid = selectuid(uname)
    friends = []
    i = 0
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    # userid = cursor.execute('select id from wechat_myuser where username = uname')
    # values = cursor.execute('select friend_id from wechat_user_realation where uid = ?',('value1',))
    cursor = conn.execute("SELECT uid_id, friend_id_id  from wechat_user_realation")
    for row in cursor:
        if (row[0] == uuuid):
            uuid = row[1]
            uuname = selectuname(uuid)
            r = {'id': uuid, 'username': uuname}
            friends.append(r)
            i = i + 1

        if (row[1] == uuuid):
            uuid = row[0]
            uuname = selectuname(uuid)
            r = {'id': uuid, 'username': uuname}
            friends.append(r)

            i = i + 1
    conn.close()
    return friends


# 根据id，返回用户的所有的群name  数组  用户群的关系表

def selectGroups(uname):
    # 该用户的id
    uuuid = selectuid(uname)
    groups = []
    i = 0

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    # userid = cursor.execute('select id from wechat_myuser where username = uname')
    # values = cursor.execute('select friend_id from wechat_user_realation where uid = ?',('value1',))
    cursor = conn.execute("SELECT uid_id, gid_id  from wechat_g_msg_config")
    for row in cursor:
        if (row[1] == uuuid):
            uuid = row[0]
            groups.append(uuid)
            i = i + 1
    conn.close()
    return groups


# 删除好友
def friendssdelete(uid1, uid2):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("DELETE from COMPANY where ID=uid1 and ID2=uid2;")
    conn.commit()
    conn.close()


# 退群
def groupsdelete(uid1, uid2):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("DELETE from COMPANY where ID=uid1 and ID2=uid2;")
    conn.commit()
    conn.close()


# 添加好友

def friendsadd(uid1, uid2):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (1, 'Paul', 32, 'California', 20000.00 )");

    conn.commit()

    conn.close()


# 加群
def groupsadd(uid, gid):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (1, 'Paul', 32, 'California', 20000.00 )");

    conn.commit()

    conn.close()


# 返回双人聊天历史记录：(返回 消息 时间 uid 显示的时候根据顺序判断谁说出的 )
def messagesTwo(uid1, uid2):
    msssages = []
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print
        "ID = ", row[0]
        print
        "NAME = ", row[1]
        print
        "ADDRESS = ", row[2]
        print
        "SALARY = ", row[3], "\n"
    conn.close()
    return cursor


def messagesGroup(uid, gid):
    msssages = []
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print
        "ID = ", row[0]
        print
        "NAME = ", row[1]
        print
        "ADDRESS = ", row[2]
        print
        "SALARY = ", row[3], "\n"
    conn.close()
    return cursor

def get_mes(request):
    b =request.user.id
    a = request.GET.get('uid')