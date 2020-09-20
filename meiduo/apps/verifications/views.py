from django.shortcuts import render
from django.views import View
from verifications.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django import http
import random,logging

from . import constants
from meiduo.utils.response_code import RETCODE
from verifications.libs.yuntongxun.ccp_sms import CPP
# Create your views here.

# 创建日志输出器，来记录短信日志
logger = logging.getLogger('django')

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
        # 创建链接redis的对象
        redis_conn = get_redis_connection('verify_code')

        # 判断用户是否频繁发送短信验证码
        send_flg = redis_conn.get('send_flg_%s' % mobile)
        if send_flg:    # 已经发送过了
            return http.JsonResponse({'code':RETCODE.THROTTLINGERR,'errmsg':'发送短信过于频繁'})

        # 提取图形验证码

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
        # 手动输出日志，记录短信验证码
        logger.info(sms_code)
        # # 保存短信验证码
        # redis_conn.setex("sms_%s" % mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
        # # 保存发送短信验证码的标记
        # redis_conn.setex('send_flg_%s' % mobile,constants.SEND_SMS_CODE_INTERVAL,1)

        # 创建redis管道
        pl = redis_conn.pipeline()
        # 将命令添加到队列中
        # 保存短信验证码
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送短信验证码的标记
        pl.setex('send_flg_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 执行
        pl.execute()

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
