# -*- coding:utf-8 -*-

# import ssl
# ssl._create_default_https_context =ssl._create_stdlib_context # 解决Mac开发环境下，网络错误的问题


from meiduo.apps.verifications.libs.yuntongxun.CCPRestSDK import  REST
# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8a216da8747ac98201749ae4700822ad'

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = '4d8cd9d8055b4cf385d44575f746ef41'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8aaf0708747ac63201749ae7a9ae205b'

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'sandboxapp.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'

# 云通讯官方提供的发送短信代码实例
# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id
# def sendTemplateSMS(to, datas, tempId):
#     # 初始化REST SDK
#     rest = REST(_serverIP, _serverPort, _softVersion)
#     rest.setAccount(_accountSid, _accountToken)
#     rest.setAppId(_appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     print(result)


class CPP(object):
    """发送短信验证码的单例类"""
    def __new__(cls, *args, **kwargs):
        """
        定义单例的初始化方法
        :return: 单例对象
        """
        # 判断单例是否存在，_instance属性中存储的就是单例
        if not hasattr(cls,"_instance"):
            # super(CPP, cls)首先找到CPP的父类object，然后把cls转换为父类object
            cls._instance = super(CPP, cls).__new__(cls, *args, **kwargs)
            # 绑定rest与单例
            cls._instance.rest = REST(_serverIP, _serverPort, _softVersion)
            cls._instance.rest.setAccount(_accountSid, _accountToken)
            cls._instance.rest.setAppId(_appId)
        return cls._instance


    def send_message_sms(self,to, datas, tempId):
        """
        :param to: 手机号
        :param datas: 内容数据
        :param tempId: 模板ID
        :return: 成功0，失败-1
        """
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        print(result)
        if result.get("statusCode") == "000000":
            return 0
        else:
            return -1

if __name__ == '__main__':
    # 注意： 测试的短信模板编号为1
    CPP().send_message_sms('17070955625', ['123456', 5], 1)

    # sendTemplateSMS()
