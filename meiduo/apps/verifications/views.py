from django.shortcuts import render
from django.views import View
from verifications.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django import http
# Create your views here.

class ImageCodeView(View):
    """图形验证码"""
    def get(self,request,uuid):
        """
        :param request:
        :param uuid: 通用唯一识别码，用于唯一表示该图形验证码属于哪个用户的
        :return:
        """
        # 接受和校验参数
        # 实现主体业务逻辑：生成图形验证码，保存，响应图形验证码
        # 生成图形验证码
        text,image = captcha.generate_captcha()
        # 保存图片验证码
        redis_conn = get_redis_connection('verify_code')    # 找到dev中配置的redis库
        # 设置键为uuid，值为text，超时时间为300秒
        redis_conn.setex("img_%s" % uuid,300,text)  # setex可以设置生存时间
        # 响应图片验证码
        return http.HttpResponse(image,content_type='image/jpg')
