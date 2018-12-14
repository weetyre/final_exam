from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from .admin import UserCreationForm
from .forms import LoginForm, ChangeEmailForm, MyPasswordChangeForm
from .models import MyUser
import sqlite3

def index_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # if email is not found
            flag = 1
            user_model = MyUser.objects.all()
            for i in user_model:
                if i.email == email:
                    flag = 0

            if flag:
                error_message = 'email not found.'
                return render(request, 'login.html',
                              {'form': form, 'input_error': error_message, 'block_title': 'Login'})

            # user = MyUser.objects.get(email=email)
            user = auth.authenticate(email=email, password=password)
            # incorrect password
            if user is None:
                error_message = 'password is invalid.'
                return render(request, 'login.html',
                              {'form': form, 'input_error': error_message, 'block_title': 'Login'})

            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                return HttpResponseRedirect("/profile?user=" + user.username)
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
            user = MyUser.objects.create_user(username, email, sex, request.POST['password'])

            user = auth.authenticate(email=email, password=request.POST['password'])
            auth.login(request, user)

            return HttpResponseRedirect("/profile?email=" + user.email)
        else:
            if len(email_filter) > 0:
                error_msg1 = 'email already taken.'
                return render(request, 'register.html',
                              {'form': form, 'input_error': error_msg1, 'block_title': 'Register'})

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


def myhome(request):
    return render(request, 'home_base.html')

#��ѯ���еĺ��ѡ���ѯid������Ⱥ����
def select(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor=conn.cursor()
    value1 = cursor.execute('select id from wechat_myuser where username = ?',('request',))

    values = cursor.execute('select friend_id from wechat_user_realation where uid = ?',('value1',))
    friend = []
    for row in values:
        friend.append(row)
    conn.close()

#������Ⱥ
def ginsert(uid,gname):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    #creat_at = datetime.datetime.now()
    cursor.execute('insert into wechat_group (gid,gname,creat_time,num_of_group,master_id) values (random.uniform(10, 1000),request,creat_at,1,request2)')
    conn.commit()
    conn.close()

#
#��Ⱥ �����û�id��Ⱥid  ��ӵ��Ǹ�user��group�Ĺ�ϵ��
def gadd(uid,gid):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    #c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
         # VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");


    conn.commit()
    conn.close()

#����������ѯȺ�е������û�  ��ѯgid��uid�Ĺ�ϵ���������е�uid

#��Ⱥ �������û�id��Ⱥid
def gdelete(uid,gid):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    #c.execute("DELETE from COMPANY where ID=2;")
    conn.commit()
    conn.close()


#��Ӻ���
def fadd(uid1,uid2):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
   # cursor.execute('insert into wechat_user_realation(uid,friend_id) values (request,request2)')
    conn.commit()
    conn.close()


#ɾ������
def fdelete(uid1,uid2):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    #cursor.execute('delete from wechat_user_realation where uid = ? and friend_id = ?',('request','request2',))
    conn.commit()
    conn.close()

#�������к���


def GueryUids(uid):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    print("Opened database successfully");
    #ȷ������֮�����޸�
    cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print
        "ID = ", row[0]
        print
        "NAME = ", row[1]
        print
        "ADDRESS = ", row[2]
        print
        "SALARY = ", row[3], "\n"

    print
    "Operation done successfully";
    conn.close()






#��������Ⱥ

def Guerygids(uid):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    print("Opened database successfully");
    #ȷ������֮�����޸�
    cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print
        "ID = ", row[0]
        print
        "NAME = ", row[1]
        print
        "ADDRESS = ", row[2]
        print
        "SALARY = ", row[3], "\n"

    print
    "Operation done successfully";
    conn.close()


#���ҳ������е�uid





#����Ⱥ��id ����ȺȺname
def GueryGname(gid):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    print("Opened database successfully");
    #ȷ������֮�����޸�
    cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print
        "ID = ", row[0]
        print
        "NAME = ", row[1]
        print
        "ADDRESS = ", row[2]
        print
        "SALARY = ", row[3], "\n"

    print
    "Operation done successfully";
    conn.close()



#�����û����ַ����û���id
def Gueryuid(uname):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    print("Opened database successfully");

    cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print
        "ID = ", row[0]
        print
        "NAME = ", row[1]
        print
        "ADDRESS = ", row[2]
        print
        "SALARY = ", row[3], "\n"

    print
    "Operation done successfully";
    conn.close()


#˫�����췢����Ϣ����Ϣ�������ݿ�
def ginsert(uid,tid,message):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    #creat_at = datetime.datetime.now()
    cursor.execute('insert into wechat_group (gid,gname,creat_time,num_of_group,master_id) values (random.uniform(10, 1000),request,creat_at,1,request2)')
    conn.commit()
    conn.close()

#Ⱥ���췢����Ϣ����Ϣ�������ݿ�

#˫�����췢����Ϣ����Ϣ�������ݿ�
def ginsert(uid,gname,message):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    #creat_at = datetime.datetime.now()
    cursor.execute('insert into wechat_group (gid,gname,creat_time,num_of_group,master_id) values (random.uniform(10, 1000),request,creat_at,1,request2)')
    conn.commit()
    conn.close()


#����һ��id����Ϣ��jsȫ�ֱ����ж�


#urls py����
# path('home', views.myhome)

