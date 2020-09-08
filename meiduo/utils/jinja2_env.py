# from jinja2 import Environment
# from django.urls import reverse
# from django.contrib.staticfiles.storage import staticfiles_storage
#
# def jinja2_environment(**options):
#     """jinja2环境"""
#     # 创建环境对象
#     env = Environment(**options)
#     # 自定义语法: {{ static('静态文件相对路径') }} {{ url('路由的命名空间') }}
#     env.globals.update({
#         'static':staticfiles_storage,  # 获取静态文件的前缀
#         'url':reverse, # 表面上是调用的路由命名空间，实际上调用的是reverse (反向解析，由别名解析回路由)
#
#     })
#     # 返回环境对象
#     return env
from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def jinja2_environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env