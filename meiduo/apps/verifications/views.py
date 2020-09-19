from django.shortcuts import render
from django.views import View
from verifications.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django import http
from . import constants
from meiduo.utils.response_code import RETCODE
import random
from verifications.libs.yuntongxun.ccp_sms import CPP
# Create your views here.

class SMSCodeView(View):
    """短信验证码"""
    def get(self,request,mobile):
        """
        :param request:
        :param mobile:手机号
        :return: json
        """
        # 接收参数
        img_code_client = request.GET.get('image_code')
        # print(img_code_client)
        uuid = request.GET.get('uuid')
        # 校验参数
        if not all([img_code_client,uuid]):
            return http.HttpResponseForbidden('缺少必要参数')

        # 提取图形验证码
        redis_conn = get_redis_connection('verify_code')
        img_code_server = redis_conn.get("img_%s" % uuid)   # 这是一个bytes类型
        if img_code_server is None:
            return http.JsonResponse({'code':RETCODE.IMAGECODEERR,'errmsg':'图形验证码已经失效'})
        # 删除图形验证码
        redis_conn.delete("img_%s" % uuid)
        # 对比图形验证码，将bytes类型转为字符串再比较
        img_code_server = img_code_server.decode()
        if img_code_server.lower() != img_code_client.lower():
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码有误'})

        # 生产短信验证码 %06d代表，如果不够6位，前面补0
        sms_code = '%06d' % random.randint(0,999999)
        # 保存短信验证码
        redis_conn.setex("sms_%s" % mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
        # 发送短信验证码
        CPP().send_message_sms(mobile,[sms_code,constants.SMS_CODE_REDIS_EXPIRES // 60],constants.SEND_SMS_TEMPLATE_ID)
        return http.JsonResponse({'code':RETCODE.OK,'errmsg':'发送短信成功'})


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
        redis_conn.setex("img_%s" % uuid,constants.IMAGE_CODE_REDIS_EXPIRES,text)  # setex可以设置生存时间
        # 响应图片验证码
        return http.HttpResponse(image,content_type='image/jpg')
