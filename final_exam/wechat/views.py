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
totalOnline = 0
onlineUsers = []
tid = 0


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
        groups = selectGroups(user.username)
        return render(request, 'home_base.html', {'user': user, 'friends': friends, 'groups': groups})


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
    global allconn, totalOnline, onlineUsers, tid
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index.html', allresult)
    else:
        # 将链接(请求？)存入全局字典中
        allconn[str(userid)] = request.websocket
        totalOnline = totalOnline + 1

        msg = {'type': 'broadcast', 'id': request.user.id, 'username': request.user.username, 'msg': 'on',
               'total': totalOnline}
        request.websocket.send(json.dumps(msg))
        # 遍历请求地址中的消息
        for message in request.websocket:
            try:
                # 将信息发至自己的聊天框
                request.websocket.send(message)
            except Exception as e:
                totalOnline = totalOnline - 1
                message = {'type': 'broadcast', 'id': request.user.id, 'username': request.user.username, 'msg': 'off',
                           'total': totalOnline}

            mes = json.loads(message)

            if mes['to'] != '0':
                models.One_to_one_msg_record.objects.create(form_id_id=mes['from'], to_id_id=int(mes['to']),
                                                            content=mes['msg'])
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
    conn.close()
    return uuid


def selectgname(gid):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    # userid = cursor.execute('select id from wechat_myuser where username = uname')
    # values = cursor.execute('select friend_id from wechat_user_realation where uid = ?',('value1',))
    cursor = conn.execute("SELECT gid, gname from wechat_group")
    for row in cursor:
        if (row[0] == gid):
            gname = row[1]
    conn.close()
    return gname


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


# 根据群的id 返回群中包含的所有的uid
def selectGroupIDs(gid):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    gids = []
    # userid = cursor.execute('select id from wechat_myuser where username = uname')
    # values = cursor.execute('select friend_id from wechat_user_realation where uid = ?',('value1',))
    cursor = conn.execute("SELECT gid_id, uid_id from wechat_g_msg_config")
    for row in cursor:
        if (row[0] == gid):
            gids.append(row[1])
    conn.close()
    return gids


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
    friends = []
    i = 0
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    # userid = cursor.execute('select id from wechat_myuser where username = uname')
    # values = cursor.execute('select friend_id from wechat_user_realation where uid = ?',('value1',))
    cursor = conn.execute("SELECT gid_id,uid_id from wechat_g_msg_config")
    for row in cursor:
        if (row[0] == uuuid):
            uuid = row[1]
            uuname = selectgname(uuid)
            uuname = selectuname(uuid)
            r = {'gid': uuid, 'gname': uuname}
            friends.append(r)

        if (row[1] == uuuid):
            uuid = row[0]
            uuname = selectgname(uuid)
            r = {'gid': uuid, 'gname': uuname}
            friends.append(r)
    conn.close()
    return friends


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

    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )");

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
    b = request.user.id
    a = request.GET['uid']

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.execute("SELECT form_id_id,to_id_id, content  from wechat_one_to_one_msg_record")
    data_rows = cursor.fetchall()

    msgs = []
    i = 0
    for row in data_rows:
        r = {'from': row[0], 'to': row[1], 'msg': row[2]}
        msgs.append(r)
        i += 1

    return HttpResponse(json.dumps(msgs))


def create_group(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        group = models.Group.objects.create(gname=group_name, num_of_group=1, master_id_id=request.user.id)
        models.G_msg_config.objects.create(gid_id=int(group.gid), uid_id=request.user.id)
        succeed_message = 'Success!'
        return render(request, 'add_friends.html',
                      {'user': request.user, 'suc': succeed_message})


def add_group(request):
    if request.method == 'POST':
        group_id = request.POST['group_id']
        group = models.Group.objects.filter(gid=int(group_id))
        if group.count() == 0:
            error_message = 'Group id not exists!'
            return render(request, 'add_friends.html', {'user': request.user, 'find_n': error_message})
        else:
            if 0 != models.G_msg_config.objects.filter(uid_id=request.user.id).count():
                error_message = 'You have attended!'
                return render(request, 'add_friends.html', {'user': request.user, 'find_n': error_message})
            else:
                models.G_msg_config.objects.create(gid_id=int(group_id), uid_id=request.user.id)
                succeed_message = 'Success!'
                return render(request, 'add_friends.html', {'user': request.user, 'find_y': succeed_message})


def add_friends(request):
    if request.method == 'POST':
        friend_id = request.POST['friend_id']
        friends = models.MyUser.objects.filter(id=friend_id)

        if friends.count() == 0:
            error_message = 'User id not exists!'
            return render(request, 'add_friends.html', {'user': request.user, 'f_n': error_message})
        else:
            if 0 != models.User_realation.objects.filter(friend_id_id=friend_id, uid_id=request.user.id).count():
                error_message = 'You have added the friend!'
                return render(request, 'add_friends.html', {'user': request.user, 'f_n': error_message})
            else:
                if int(friend_id) == request.user.id:
                    error_message = 'You can not add yourself!'
                    return render(request, 'add_friends.html', {'user': request.user, 'f_n': error_message})
                else:
                    models.User_realation.objects.create(friend_id_id=int(friend_id), uid_id=request.user.id)
                    succeed_message = 'Success!'
                    return render(request, 'add_friends.html', {'user': request.user, 'f_y': succeed_message})
