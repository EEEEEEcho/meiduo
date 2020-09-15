from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django import http
import re
from users.models import User
from django.db import DatabaseError
from django.contrib.auth import login
from meiduo.utils.response_code import RETCODE
# Create your views here.

class RegisterView(View):
    """用户注册"""
    def get(self,request):
        """get请求，提供用户注册页面"""
        return render(request,"register.html")

    def post(self,request):
        """实现用户注册的逻辑"""
        # 这里有个问题，为什么能从post请求中接收数据呢？
        # 为什么能够确定键就是username呢？
        # 是因为表单在提交时是通过post请求提交的，然后每个键是由<input type="text" name="mobile" id="phone" v-model="mobile" @blur="check_mobile">
        # 里面的name属性所决定的
        # 1.接受参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')
        # 2.校验参数，前后端的校验需要分开，避免恶意用户越过前端逻辑发送请求，前端校验的逻辑与后端相同
        # 判断参数是否齐全 all([列表])方法,获取检验列表中的元素是否为空，只要有一个为空返回false，否则返回true
        if not all([username,password,password2,mobile,allow]):
            # 如果缺少必穿参数，响应错误提示信息，返回403
            return http.HttpResponseForbidden('缺少必要参数')
        # 判断用户名是否为5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否为8-20个数字
        if not re.match(r'^[0-9a-zA-Z]{8,20}$',password):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断两次密码是否相同
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}',mobile):
            return http.HttpResponseForbidden('请输入正确的手机号')
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # user = User.objects.create_user(username=username, password=password, mobile=mobile)
        # 3.保存注册数据，业务逻辑核心
        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            # 如果数据库出错了,告诉用户注册失败
            return render(request,"register.html",{'register_error':'注册失败'})

        # 实现状态保持,从而实现注册即登录，django已经帮我们实现了将注册好的用户会话存入session中的机制
        login(request,user)

        # 4.响应结果,重定向到首页 , 反向解析，到主页 reverse('contents:index') == ‘/’
        return redirect(reverse('contents:index'))

class UsernameCountView(View):
    """判断用户名是否重复注册"""
    # 这里的username接收url中传递过来的username
    def get(self,request,username):
        """
        :param request:
        :param username: 用户名
        :return: JSON
        """
        # 接受和校验参数，路径参数
        # 实现主体业务逻辑：使用username查询对应的记录的条数 filter返回的是满足条件的结果集，
        count = User.objects.filter(username=username).count()
        # 响应结果
        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'OK',
            'count':count
        })

class MobileCountView(View):
    """判断手机号是否重复"""
    # 这里的mobile是接受url中传过来的mobile
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'OK',
            'count':count
        })