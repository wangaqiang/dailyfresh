from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from user.models import User
# from . import models
from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer # 需要先装这个包
from itsdangerous import SignatureExpired
import re

# Create your views here.
def register(request):
    '''注册页面'''
    if request.method == "GET":
        # 显示注册页面
        return render(request, 'register.html')
    else:
        '''进行注册处理'''
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):   # all()传入可迭代对象 每个元素都返回真的时候才返回真，否则返回假
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 校验是否勾选遵守协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = models.User.objects.get(username=username)  # get方法只返回一个满足条件的对象，如果不存在则报异常
        except models.User.DoesNotExist:
            # 捕获到异常说明用户名不存在数据库  可以使用
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html',{'errmsg':'用户名已经存在'})


        # 进行业务处理：进行用户注册
        # 第一种方法创建对象 然后添加属性 最后对象.save（）保存至数据库即可
            # user = User()
            # user.username = username
            # user.password = password
            # user.email = email
            # user.save()
        # 第二种方法
        user = models.User.objects.create_user(username, email, password)
        user.is_active = 0 # django 默认注册的帐号是激活需要手动关闭
        user.save()

        # 返回应答, 跳转到首页
        return redirect(reverse('goods:index')) # reverse是反向解析函数

        
def register_handle(request):
    '''进行注册处理'''
    # 接受数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')

    # 进行数据校验
    if not all([username, password, email]):   # all()传入可迭代对象 每个元素都返回真的时候才返回真，否则返回假
        # 数据不完整
        return render(request, 'register.html', {'errmsg': '数据不完整'})

    # 校验邮箱
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

    # 校验是否勾选遵守协议
    if allow != 'on':
        return render(request, 'register.html', {'errmsg': '请同意协议'})

    # 校验用户名是否重复
    try:
        user = User.objects.get(username=username)  # get方法只返回一个满足条件的对象，如果不存在则报异常
    except User.DoesNotExist:
        # 捕获到异常说明用户名不存在数据库  可以使用
        user = None

    if user:
        # 用户名已存在
        return render(request, 'register.html',{'errmsg':'用户名已经存在'})

    # 进行业务处理：进行用户注册
    # 第一种方法创建对象 然后添加属性 最后对象.save（）保存至数据库即可
        # user = User()
        # user.username = username
        # user.password = password
        # user.email = email
        # user.save()
    # 第二种方法
    user = User.objects.create_user(username, email, password)
    user.is_active = 0 # django 默认注册的帐号是激活需要手动关闭
    user.save()

    # 返回应答, 跳转到首页
    return redirect(reverse('goods:index')) # reverse是反向解析函数


class RegisterView(View):
    '''注册'''
    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html')

    def post(self, request):
        '''进行注册处理'''
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):   # all()传入可迭代对象 每个元素都返回真的时候才返回真，否则返回假
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 校验是否勾选遵守协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)  # get方法只返回一个满足条件的对象，如果不存在则报异常
        except User.DoesNotExist:
            # 捕获到异常说明用户名不存在数据库  可以使用
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html',{'errmsg':'用户名已经存在'})

        # 进行业务处理：进行用户注册
        # 第一种方法创建对象 然后添加属性 最后对象.save（）保存至数据库即可
            # user = User()
            # user.username = username
            # user.password = password
            # user.email = email
            # user.save()
        # 第二种方法
        user = User.objects.create_user(username, email, password)
        user.is_active = 0 # django 默认注册的帐号是激活需要手动关闭
        user.save()

        # 发送激活邮件，包含激活链接：http://127.0.0.1:8000/user/active/id
        # 激活连接中需要包含用户的身份信息,并且要把身份信息进行加密

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600) # 设置密钥和过期时间
        info = {'confirm':user.id}
        token = serializer.dumps(info) # 进行加密 返回bytes
        token = token.decode() # 默认是utf8

        # 发邮件
        send_register_active_email.delay(email, username, token) # 将任务放入队列

        # 返回应答, 跳转到首页
        return redirect(reverse('goods:index')) # reverse是反向解析函数


class ActiveView(View):
    '''用户激活'''
    def get(self, request, token):
        '''进行用户激活'''
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接已经过期
            return HttpResponse('激活链接已过期')

#user/login
class LoginView(View):
    '''登录'''
    def get(self, request):
        '''显示登录页面'''
        return render(request, 'login.html')